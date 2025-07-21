#diego no le hagas caso a eso solo era para ver los modelos disponnibles
import google.generativeai as genai

genai.configure(api_key="AIzaSyAOgacXaK6erRzeJ9--2ONfFo_gLLp6g3k")

# Ver modelos disponibles
models = genai.list_models()
for model in models:
    print(model.name, "-", model.supported_generation_methods)
