require('open-uri')
require('nokogiri')
require('csv')

class Scraper
    attr_accessor :link

    def initialize(link)
        @link = link
    end

    def gen_csv(filename)
        CSV.open(filename, 'w') do |csv|
        end
    end

    def save_csv(filename, data)
        CSV.open(filename, 'a') do |csv|
            csv << data
        end
    end

    def extract()
        print "Ingrese la cantidad de páginas a extraer (1-10): "
        pages = gets.chomp.to_i
        pages = ((pages > 0) and (pages < 11)) ? pages : 1

        filename = 'data/sandoval.csv'

        gen_csv(filename)
        save_csv(filename, ["Title", "Link", "Content"])

        for i in 0..(pages - 1)
            new_link = @link + (i > 0 ? "/page/#{i+1}/" : "")
            data = URI.open(new_link).read
            parsed_content = Nokogiri::HTML(data)

            parsed_content.css('div.is-layout-flow ~ ul.wp-block-post-template > li.wp-block-post').each do |post|
                info = post.css('h3 a')

                title = info.text.strip
                link = info.attr('href')

                next if link.nil?

                page_data = URI.open(link).read
                page_content = Nokogiri::HTML(page_data)

                paragraphs = page_content.css('div.wp-block-column > div.entry-content p').map(&:inner_text).map(&:strip)
                content = paragraphs.join(" ")

                save_csv(filename, [title, link, content])
            end
        end
    end
end

scraper = Scraper.new('https://techcrunch.com/category/artificial-intelligence/')

scraper.extract() 
