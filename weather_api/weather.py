#weather api 
import requests
import sys

class Sensor:
    def __init__(self, city):
        self.__city = city
    @property
    def city(self):
        return self.__city
    def get_data(self):
        get_resp = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={self.city}&appid=008527cdc57b448d328cf28676dc0864")
        if get_resp.status_code == 200:
            return get_resp.json()
        else:
            return None

class TemperatureSensor(Sensor):
    def __init__(self, city):
        super().__init__(city)
        self.__temp_data = super().get_data()['main']
    @property
    def temp_data(self):
        return self.__temp_data
    @staticmethod
    #temp data is in kalvin
    def __kalvin_converter(temp):
        return (float(temp) - 273.15)*(9/5) + 32
    def __get_temp_condition(self):
        temp = __class__.__kalvin_converter(self.temp_data['temp'])
        if temp > 90:
            return (temp, "Very Hot!")
        elif temp >= 80:
            return (temp, "Hot.")
        elif temp >= 60:
            return (temp, "Mild.")
        elif temp >= 40:
            return (temp, "Cool.")
        elif temp <= 32 and temp > 0:
            return (temp, "Very Cold.")
        else:
            return ("Freezing!")
    def __get_min_max_condition(self):
        data = self.temp_data
        min = __class__.__kalvin_converter(data['temp_min'])
        max = __class__.__kalvin_converter(data['temp_max'])
        temp_drops = max-min
        if temp_drops < 5:
            return (min, max, "Low Temperature Drops")
        elif temp_drops < 15:
            return (min, max, "Medium Temperature Drops")
        else:
            return (min, max, "High Temperature Drops")
    def report_temperature(self):
        condition_temp = self.__get_temp_condition()
        min, max, description = self.__get_min_max_condition()
        return f"{condition_temp[0]:.1f}F. {condition_temp[1]}\n{min:.1f}F Min. {max:.1f}F Max. {description}"
    
class WindSensor(Sensor):
    def __init__(self, city):
        super().__init__(city)
        self.__wind_data = super().get_data()['wind']
    @property
    def wind_data(self):
        return self.__wind_data
    @staticmethod
    #changnes raw m/s to mph
    def __wind_converter(speed):
        rate = 3600/(1000*1.61)
        return speed*rate
    def __get_wind_condition(self):
        wind_speed = __class__.__wind_converter(self.wind_data['speed'])
        if wind_speed < 5:
            return (wind_speed, "Calm.")
        elif wind_speed <= 5 and wind_speed < 15:
            return (wind_speed, "Breezy.")
        elif  wind_speed <= 15 and wind_speed < 25:
            return (wind_speed, "Windy.")
        else:
            return (wind_speed, "Very Windy.")
        
    def report_wind(self):
        condition = self.__get_wind_condition()
        return f"{condition[0]:.1f} MPH. {condition[1]}"
    
class CloudSensor(Sensor):
    def __init__(self, city):
        super().__init__(city)
        self.__cloud_description = super().get_data()['weather'][0]['description']
        self.__cloud_percentage = super().get_data()['clouds']['all']
    @property
    def cloud_description(self):
        return self.__cloud_description
    @property 
    def cloud_percentage(self):
        return self.__cloud_percentage   
    
    def report_cloud(self):
        return f"{self.__cloud_percentage}% Clouds. {self.__cloud_description.capitalize()}"

class HumiditySensor(Sensor):
    def __init__(self, city):
        super().__init__(city)
        self.__humidity_data = super().get_data()['main']['humidity']
    @property
    def wind_data(self):
        return self.__humidity_data
    def __get_humidity_condition(self):
        if self.__humidity_data < 30:
            return (self.__humidity_data, "Low Humidity")
        elif self.__humidity_data < 50:
            return (self.__humidity_data, "Moderate Humidity")
        elif self.__humidity_data < 70:
            return (self.__humidity_data, "High Humidity")
        elif self.__humidity_data < 90:
            return (self.__humidity_data, "Very Humidity")
        else:
            return (self.__humidity_data, "Saturated Humidity")
    def report_humidity(self):
        condition = self.__get_humidity_condition()
        return f"{condition[0]:.1f}%. {condition[1]}"
        
class VisibilitySensor(Sensor):
    def __init__(self, city):
        super().__init__(city)
        self.__visibility_data = super().get_data()['visibility']
    @property
    def visibility_data(self):
        #convert the m to km 
        return (self.__visibility_data/1000)
    def __get_visibility_condition(self):
        if self.visibility_data > 10:
            return (self.visibility_data, "Good Visibility")
        elif self.visibility_data > 5 and self.visibility_data <= 10:
            return (self.visibility_data, "Moderate Visibility")
        elif self.visibility_data > 1 and self.visibility_data <= 5:
            return (self.visibility_data, "Reduced Visibility")
        elif self.visibility_data > .7 and self.isibility_data <= 1:
            return (self.visibility_data, "Poor Visibility")
        else:
            return (self.__visibility_data, "Very Poor Visibility")
    def report_visibility(self):
        condition = self.__get_visibility_condition()
        return f"{condition[0]:.1f} KM. {condition[1]}"
        
class WeatherStation():
    def __init__(self, city):
        self.__temperature_sensor = TemperatureSensor(city)
        self.__wind_sensor = WindSensor(city)
        self.__cloud_sensor = CloudSensor(city)
        self.__humidity_sensor = HumiditySensor(city)
        self.__visibility_sensor = VisibilitySensor(city)
    @property
    def temperature_sensor(self):
        return self.__temperature_sensor
    @property
    def wind_sensor(self):
        return self.__wind_sensor
    @property
    def cloud_sensor(self):
        return self.__cloud_sensor
    @property
    def humidity_sensor(self):
        return self.__humidity_sensor
    @property
    def visibility_sensor(self):
        return self.__visibility_sensor
    def report_weather(self):
        print(self.temperature_sensor.report_temperature())
        print(self.wind_sensor.report_wind())
        print(self.cloud_sensor.report_cloud())
        print(self.humidity_sensor.report_humidity())
        print(self.visibility_sensor.report_visibility())

class UserProgram:
    def __init__(self):
        self.__checked_weather = False
    def __get_validated_city(self):
        while True:
            quit_string = ""
            if self.__checked_weather:
                quit_string = "Enter 'exit' to exit. Or. "
            city = input(f"{quit_string}Enter a city: ")
            if city.lower() == 'exit':
                print('Exitting Program...')
                sys.exit()
            get_resp = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=008527cdc57b448d328cf28676dc0864")
            if get_resp.status_code == 200:
                return city
            else:
                print(f"Error. Could not get weather data for {city}")
    def start(self):
        ##weather api
        print("Welcome to the Weather App")
        while True:
            city = self.__get_validated_city()
            weather = WeatherStation(city)
            weather.report_weather()
            self.__checked_weather = True

program = UserProgram()

program.start()

