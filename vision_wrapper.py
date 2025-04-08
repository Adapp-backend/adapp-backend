import os
import openai

# Set up client for the new SDK
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_image_with_openai(image_url):
    prompt = (
        "You are an ADHD productivity coach. A user uploaded a photo of their room "
        "to figure out how to get started cleaning. Analyze the photo and list 3 small, "
        "immediately doable tasks that would reduce visual clutter and create a sense of momentum. "
        "Return the list as plain text with no explanations. Format as a bullet list."
    )

    # Use gpt-4o (multimodal) as the default model
    model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-4o")

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url,
                                "detail": "auto"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300,
        )
        return response.choices[0].message.content.strip()

    except openai.APIError as e:
        print("❌ OpenAI API Error:", e)
        return f"⚠️ API error: {str(e)}"

    except openai.AuthenticationError:
        return "🔐 Authentication error: Check your API key or permissions."

    except openai.BadRequestError as e:
        print("🚫 Bad Request Error:", e)
        return f"⚠️ Bad request: {str(e)}"

    except Exception as e:
        print("❌ Unexpected Error:", e)
        return "⚠️ Error analyzing image."
