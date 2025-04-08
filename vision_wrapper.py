import os
import openai

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_image_with_openai(image_url=None):
    model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-4o")

    prompt = (
        "You are an ADHD productivity coach. A user is feeling overwhelmed and unsure how to start cleaning. "
        "Suggest 3 small, immediately doable tasks that would reduce visual clutter and create a sense of momentum. "
        "Return the list as plain text with no explanations. Format as a bullet list."
    )

    try:
        # Include image only if it's available
        content = [{"type": "text", "text": prompt}]
        if image_url:
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": image_url,
                    "detail": "auto"
                }
            })

        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": content}],
            max_tokens=300,
        )
        return response.choices[0].message.content.strip()

    except openai.BadRequestError as e:
        # If image input causes issues (e.g., access denied to vision), fallback to text-only
        if image_url:
            print("⚠️ Image model failed, falling back to text-only:", e)
            return analyze_image_with_openai(image_url=None)
        return f"⚠️ Bad request: {str(e)}"

    except openai.AuthenticationError:
        return "🔐 Authentication error: Check your API key or permissions."

    except openai.APIError as e:
        print("❌ OpenAI API Error:", e)
        return f"⚠️ API error: {str(e)}"

    except Exception as e:
        print("❌ Unexpected Error:", e)
        return "⚠️ Error analyzing image."
