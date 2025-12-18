from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

# Function to extract video info
def get_video_info(url):
    ydl_opts = {
        'format': 'best',  # Best quality
        'quiet': True,
        'no_warnings': True,
        'geo_bypass': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # download=False ka matlab video server par save nahi hogi
            # Hum bas uska direct link nikal rahe hain
            info = ydl.extract_info(url, download=False)
            
            # Direct video URL (audio+video combined usually)
            video_url = info.get('url')
            title = info.get('title', 'Video')
            thumbnail = info.get('thumbnail')
            
            return {
                "status": "success",
                "title": title,
                "thumbnail": thumbnail,
                "download_url": video_url
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-video', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({"status": "error", "message": "No URL provided"})
    
    result = get_video_info(url)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
