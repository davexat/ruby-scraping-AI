require 'httparty'
require 'nokogiri'
require 'csv'

# 1. Configuración
url = 'https://arstechnica.com/ai/'
headers = {
  "User-Agent" => "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

puts "📡 Conectando a #{url}..."
response = HTTParty.get(url, headers: headers)

if response.code == 200
  doc = Nokogiri::HTML(response.body)

  # 2. Selección de artículos basada en tu HTML
  # Buscamos todas las etiquetas <article> que estén dentro del layout
  articulos = doc.css('article')

  puts "🔍 Se encontraron #{articulos.count} artículos en la portada."

  if articulos.empty?
    puts "⚠️ No se encontraron artículos. Es posible que la estructura interna haya cambiado drásticamente."
    exit
  end

  # 3. Guardado en CSV
  CSV.open("datos_arstechnica.csv", "wb") do |csv|
    csv << ["Titulo", "Link", "Contenido"]

    articulos.each do |articulo|
      # --- Lógica de Extracción ---

      # TÍTULO Y LINK: Generalmente están dentro de un <h2> que contiene un <a>
      nodo_titulo = articulo.at_css('h2 a') 

      # Si no encuentra h2, intentamos buscar el primer enlace <a> dentro del header del artículo
      nodo_titulo = articulo.at_css('header a') unless nodo_titulo

      # CONTENIDO: Buscamos el párrafo <p> que sirve de extracto (excerpt).
      # En el nuevo diseño suele ser un <p class="excerpt"> o simplemente el primer <p> que no sea meta-data.
      nodo_contenido = articulo.at_css('div.excerpt') || articulo.at_css('p.excerpt') || articulo.at_css('p')

      # --- Limpieza y Guardado ---
      if nodo_titulo
        titulo = nodo_titulo.text.strip
        link = nodo_titulo['href']

        # Validamos el contenido. Si no hay resumen, ponemos "Sin resumen"
        contenido = nodo_contenido ? nodo_contenido.text.strip : "Sin resumen disponible"

        # Escribimos en el CSV
        csv << [titulo, link, contenido]
        puts "   📝 Procesado: #{titulo[0..40]}..."
      else
        puts "   ⚠️ Se saltó un bloque <article> porque no se detectó título."
      end
    end
  end

  puts "\n🎉 ¡Listo! Revisa el archivo 'datos_arstechnica.csv'."

else
  puts "❌ Error al conectar: Código #{response.code}"
end