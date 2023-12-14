from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import csv


app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():
    message = "Dunwei Du  76004 & Qingwei Zeng  76028"
    return render_template(
            'index.html',
            message=message,
    )


# 10
#  http://127.0.0.1:5000/popular_words?city=Parma&limit=10
def get_popular_words(city_name, limit):
    with open("amazon-reviews.csv") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        word_counts = {}
        for row in csvreader:
            if city_name is None or row[1].lower() == city_name.lower():
                review = row[3].lower()
                words = review.split()
                unique_words = set(words)
                for word in unique_words:
                    if word in word_counts:
                        word_counts[word] += 1
                    else:
                        word_counts[word] = 1

    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    popular_words = [{"term": word, "popularity": count} for word, count in sorted_words[:limit]]
    return popular_words


@app.route('/popular_words', methods=['GET'])
def popular_words():
    city_name = request.args.get('city')
    limit = int(request.args.get('limit', 20))

    popular_words_list = get_popular_words(city_name, limit)
    return jsonify(popular_words_list)


# 11
# /popular_words_1
# 11
# /popular_words_1
# 11
# /popular_words_1
@app.route('/popular_words_1', methods=['GET'])
def popular_words_1():
    city_name = request.args.get('city')
    limit = int(request.args.get('limit', 20))

    city_population = {}  # 用于存储每个城市的人口
    with open("us-cities.csv") as cityfile:
        cityreader = csv.reader(cityfile, delimiter=',', quotechar='"')
        header = next(cityreader)  # 跳过头部行
        population_index = header.index("population")  # 找到 "population" 列的索引

        for city_row in cityreader:
            try:
                population_value = int(city_row[population_index])
                city_population[city_row[0].lower()] = population_value
            except (ValueError, IndexError):
                continue

    word_popularity = {}
    city_word_count = {}  # 用于存储每个词在不同城市的出现次数
    with open("amazon-reviews.csv") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        header = next(csvreader)  # 跳过头部行
        review_index = header.index("review")  # 找到 "review" 列的索引
        city_index = header.index("city")  # 找到 "city" 列的索引
        for row in csvreader:
            if city_name is None or row[city_index].lower() == city_name.lower():
                review = row[review_index].lower()
                unique_cities = set(row[city_index].lower() for row in csvreader)  # 记录评论中涉及的唯一城市
                for city in unique_cities:
                    if city in city_population:
                        city_population_value = city_population[city]
                        if city_population_value > 0:
                            if city_population_value not in city_word_count:
                                city_word_count[city_population_value] = set()
                            city_word_count[city_population_value].add(city)

    for population_value, cities_set in city_word_count.items():
        word_popularity[population_value] = sum(city_population.get(city, 0) for city in cities_set)

    sorted_popularity = sorted(word_popularity.items(), key=lambda x: x[0], reverse=True)
    popular_words_population = [{"term": str(pop), "popularity": count} for pop, count in sorted_popularity[:limit]]
    return jsonify(popular_words_population)







# 12
# http://127.0.0.1:8080/substitute_words
@app.route('/substitute_words', methods=['POST'])
def substitute_words():
    data = request.get_json()
    word_to_replace = data.get('word')
    substitute_word = data.get('substitute')

    affected_reviews_count = 0
    with open("amazon-reviews.csv", 'r') as csvfile:
        reviews = csv.reader(csvfile, delimiter=',', quotechar='"')
        rows = list(reviews)
        for i in range(len(rows)):
            review = rows[i][3].lower()
            if word_to_replace.lower() in review:
                rows[i][3] = review.replace(word_to_replace.lower(), substitute_word.lower())
                affected_reviews_count += 1

    # 保存更新后的数据到文件
    with open("amazon-reviews.csv", 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
        csvwriter.writerows(rows)

    return jsonify({"affected_reviews": affected_reviews_count})


@app.route('/words', methods=['GET'])
def words():
    return render_template('home.html')  # 替换为您实际的HTML页面文件名


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)

