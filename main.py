from __future__ import print_function # `print_function` zajišťuje zpětnou kompatibilitu pro funkci print() v Pythonu 2
import weatherapi #součástí knihovny pro práci s WeatherAPI
from weatherapi.rest import ApiException #součástí knihovny pro práci s WeatherAPI
from datetime import datetime, timedelta # moduly pro práci s datem a časem
import tkinter as tk # modul pro tvorbu GUI
from tkinter import messagebox # modul pro zobrazení oken s chybnou hláškou

# nastavení API konfigurace
configuration = weatherapi.Configuration()
configuration.api_key['key'] = 'b7c5c857f26e47adbc2103758240210'
api_instance = weatherapi.APIsApi(weatherapi.ApiClient(configuration))

# funkce pro získání počasí
def get_forecast(city, date, number_of_days, hour):
    dates_list = get_dates(date, number_of_days) # získá seznam dat na základě vstupního počátečního data a počtu dní
    forecast = []
    for date in dates_list:
        try:
            api_response = api_instance.forecast_weather(city, 1, dt=date, hour=hour) # volá API a pro každé datum ukládá odpověď
            forecast.append(api_response)
        except ApiException as e:
            print("Exception when calling APIsApi->forecast_weather: %s\n" % e)

    return forecast # vrátí seznam předpovědí počasí

# funkce pro vygenerování dat
def get_dates(date, number_of_days):
    start_date = datetime.strptime(date, '%Y-%m-%d') # převede vstupní datum
    dates = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(0, number_of_days)] # vygeneruje seznam dní podle počtu dní
    return dates

# funkce pro zpracování počasí po kliknutí na tlačítko
def najdi_pocasi():
    city = city_entry.get()  # získání daného města z textového pole
    date = datetime.today().strftime('%Y-%m-%d')  # dnešní datum
    number_of_days = 3 # počet dní pro předpověď ( dnešní datum + x následujících dní, př: 3 = dnešní den + 2 následující)
    hour = 12 # předpověď pro konkrétní hodinu

    forecast = get_forecast(city, date, number_of_days, hour) # získává předpověď počasí

    if not forecast:
        messagebox.showerror("Chyba", "Nepodařilo se načíst data o počasí.") # chybová hláška v případě nenačtení dat
        return

    city_today = forecast[0]['location']['name']  # název města
    day_today_raw = forecast[0]['location']['localtime']  # datum a čas poslední aktualizace

    day_today = datetime.strptime(day_today_raw, '%Y-%m-%d %H:%M').strftime('%d.%m.%Y') # převedení data 'day_today_raw' do formátu d.m.Y

    feelstemp_today = forecast[0]['current']['feelslike_c']  # pocitová teplota ve °C
    temp_today = forecast[0]['current']['temp_c']  # reálná teplota ve °C
    humidity_today = forecast[0]['current']['humidity']  # vlhkost v %
    precip_today = forecast[0]['current']['precip_mm']  # srážky v mm

    # výpis předpovědi pro dnešní den
    result = f"Předpověď pro město/obec {city_today} dne {day_today}:\n\n"
    result += f"Pocitová teplota:  {feelstemp_today} °C\n"
    result += f"Reálná teplota: {temp_today} °C\n"
    result += f"Úhrn srážek: {precip_today} mm\n"
    result += f"Vlhkost: {humidity_today}%\n\n"
    result += f"___________________________________________________\n\n"
    result += f"Předpověď na další dny:\n\n"

    # Výpis předpovědi na další dny
    for day in range(1, number_of_days):
        date_raw = forecast[day]['forecast']['forecastday'][0]['date'] # převedení 'date_raw' do formátu d.m.Y získání data dalšího dme
        date = datetime.strptime(date_raw, '%Y-%m-%d').strftime('%d.%m.%Y') # převedení 'date_raw' do formátu d.m.Y

        # stahování informací o počasí
        max_temp = forecast[day]['forecast']['forecastday'][0]['day']['maxtemp_c'] # maximální teplota ve °C
        min_temp = forecast[day]['forecast']['forecastday'][0]['day']['mintemp_c'] # minimální teplota ve °C
        feels_temp = forecast[day]['forecast']['forecastday'][0]['hour'][0]['feelslike_c'] # pocitová teplota ve °C
        humidity = forecast[day]['forecast']['forecastday'][0]['hour'][0]['humidity'] # vlhkost v %
        wind = forecast[day]['forecast']['forecastday'][0]['hour'][0]['wind_kph'] # rychlost větru v km/h
        precip = forecast[day]['forecast']['forecastday'][0]['day']['totalprecip_mm'] # srážky v mm
        snow = forecast[day]['forecast']['forecastday'][0]['day']['totalsnow_cm'] # sníh v cm

        # výpis předpovědi pro následující dny
        result += f"{date}:\n"
        result += f"Maximální teplota: {max_temp} °C\n"
        result += f"Minimální teplota: {min_temp} °C\n"
        result += f"Pocitová teplota: {feels_temp} °C\n"
        result += f"Vlhkost: {humidity}%\n"
        result += f"Rychlost větru: {wind} km/h\n"
        result += f"Srážky: {precip} mm\n"
        result += f"Sníh: {snow} cm\n\n"

    # zobrazení výsledků v textovém poli
    weather_output.delete(1.0, tk.END)
    weather_output.insert(tk.END, result)

# hlavní okno aplikace
root = tk.Tk()
root.title("Předpověď počasí")

# vstupního pole pro zadání města
tk.Label(root, text="Zadejte město:").pack(pady=5)
city_entry = tk.Entry(root)
city_entry.pack(pady=5)

# tlačítko pro hledání počasí
search_button = tk.Button(root, text="Najdi", command=najdi_pocasi)
search_button.pack(pady=10)

# textové pole pro zobrazení výsledků
weather_output = tk.Text(root, height=15, width=60)
weather_output.pack(pady=10)

# spuštění hlavní smyčky aplikace
root.mainloop()

