import requests
import pycountry
from deep_translator import GoogleTranslator

# Configuração dos headers
headers = {'Content-Type': 'application/json'}

# Chave da API do WeatherAPI
API_KEY = "5931757c660043ef93a215425250302"

# Obter a localidade / Cidade
localidade = input('Digite a cidade: ').strip()

# Função para obter o clima
def req_clima(city):
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if "error" in data:
            return {"error": "Cidade não encontrada ou erro na API"}
        
        return data
    except Exception as e:
        return {"error": f"Erro ao obter o clima: {str(e)}"}

# Buscar os dados do clima
dados_clima = req_clima(localidade)

if "error" in dados_clima:
    print(dados_clima["error"])
else:
    # Obter o país da resposta
    country = dados_clima["location"]["country"]

    # Função para buscar código do país
    def get_country_code(country_name):
        country = pycountry.countries.get(name=country_name)
        return country.alpha_2.lower() if country else None

    country_code = get_country_code(country)

    # Função para obter os idiomas oficiais do país
    def get_lang(country_code):
        try:
            response = requests.get(f"https://restcountries.com/v3.1/alpha/{country_code}")
            data = response.json()
            return list(data[0].get("languages", {}).values()) if data else ["en"]
        except:
            return ["en"]

    linguas_oficiais = get_lang(country_code)
    # Garante que o idioma seja um código válido de duas letras
    lingua_destino = pycountry.languages.get(name=linguas_oficiais[0])
    lingua_destino = lingua_destino.alpha_2 if lingua_destino and hasattr(lingua_destino, 'alpha_2') else "en"

    # Traduzir os dados do clima
    tradutor = GoogleTranslator(source="en", target=lingua_destino)

    # Criar um resumo do clima para traduzir
    clima_texto = f"Weather in {dados_clima['location']['name']}, {country}: {dados_clima['current']['condition']['text']}, {dados_clima['current']['temp_c']}°C."

    # Traduzir para a língua oficial do país
    clima_traduzido = tradutor.translate(clima_texto)

    print("\n=== Clima ===")
    print(clima_traduzido)