<<<<<<< HEAD
---
title: BeyondChatGPT Demo
emoji: 📉
colorFrom: pink
colorTo: yellow
sdk: docker
pinned: false
app_port: 7860
---

<p align = "center" draggable=”false” ><img src="https://github.com/AI-Maker-Space/LLM-Dev-101/assets/37101144/d1343317-fa2f-41e1-8af1-1dbb18399719" 
     width="200px"
     height="auto"/>
</p>


## <h1 align="center" id="heading">:wave: Welcome to Beyond ChatGPT!!</h1>

For a step-by-step YouTube video walkthrough, watch this! [Deploying Chainlit app on Hugging Face](https://www.youtube.com/live/pRbbZcL0NMI?si=NAYhMZ_suAY84f06&t=2119)

![Beyond ChatGPT: Build Your First LLM Application](https://github.com/AI-Maker-Space/Beyond-ChatGPT/assets/48775140/cb7a74b8-28af-4d12-a008-8f5a51d47b4c)

## 🤖 Your First LLM App

> If you need an introduction to `git`, or information on how to set up API keys for the tools we'll be using in this repository - check out our [Interactive Dev Environment for LLM Development](https://github.com/AI-Maker-Space/Interactive-Dev-Environment-for-LLM-Development/tree/main) which has everything you'd need to get started in this repository!

In this repository, we'll walk you through the steps to create a Large Language Model (LLM) application using Chainlit, then containerize it using Docker, and finally deploy it on Huggingface Spaces.

Are you ready? Let's get started!

<details>
  <summary>🖥️ Accessing "gpt-3.5-turbo" (ChatGPT) like a developer</summary>

1. Head to [this notebook](https://colab.research.google.com/drive/1mOzbgf4a2SP5qQj33ZxTz2a01-5eXqk2?usp=sharing) and follow along with the instructions!

2. Complete the notebook and try out your own system/assistant messages!

That's it! Head to the next step and start building your application!

</details>


<details>
  <summary>🏗️ Building Your First LLM App</summary>

1. Clone [this](https://github.com/AI-Maker-Space/Beyond-ChatGPT/tree/main) repo.

     ``` bash
     git clone https://github.com/AI-Maker-Space/Beyond-ChatGPT.git
     ```

2. Navigate inside this repo
     ``` bash
     cd Beyond-ChatGPT
     ```

3. Install the packages required for this python envirnoment in `requirements.txt`.
     ``` bash
     pip install -r requirements.txt
     ``` 

4. Open your `.env` file. Replace the `###` in your `.env` file with your OpenAI Key and save the file.
     ``` bash
     OPENAI_API_KEY=sk-###
     ```

5. Let's try deploying it locally. Make sure you're in the python environment where you installed Chainlit and OpenAI. Run the app using Chainlit. This may take a minute to run.
     ``` bash
     chainlit run app.py -w
     ```

<p align = "center" draggable=”false”>
<img src="https://github.com/AI-Maker-Space/LLMOps-Dev-101/assets/37101144/54bcccf9-12e2-4cef-ab53-585c1e2b0fb5"> 
</p>

Great work! Let's see if we can interact with our chatbot.

<p align = "center" draggable=”false”>
<img src="https://github.com/AI-Maker-Space/LLMOps-Dev-101/assets/37101144/854e4435-1dee-438a-9146-7174b39f7c61"> 
</p> 

Awesome! Time to throw it into a docker container and prepare it for shipping!
</details>



<details>
  <summary>🐳 Containerizing our App</summary>

1. Let's build the Docker image. We'll tag our image as `llm-app` using the `-t` parameter. The `.` at the end means we want all of the files in our current directory to be added to our image.
     
     ``` bash
     docker build -t llm-app .
     ```

2. Run and test the Docker image locally using the `run` command. The `-p`parameter connects our **host port #** to the left of the `:` to our **container port #** on the right.
    
     ``` bash
     docker run -p 7860:7860 llm-app
     ```

3. Visit http://localhost:7860 in your browser to see if the app runs correctly.

<p align = "center" draggable=”false”>
<img src="https://github.com/AI-Maker-Space/LLMOps-Dev-101/assets/37101144/2c764f25-09a0-431b-8d28-32246e0ca1b7"> 
</p>

Great! Time to ship!
</details>


<details>
  <summary>🚀 Deploying Your First LLM App</summary>

1. Let's create a new Huggingface Space. Navigate to [Huggingface](https://huggingface.co) and click on your profile picture on the top right. Then click on `New Space`.

<p align = "center" draggable=”false”>
<img src="https://github.com/AI-Maker-Space/LLMOps-Dev-101/assets/37101144/f0656408-28b8-4876-9887-8f0c4b882bae"> 
</p>

2. Setup your space as shown below:
   
- Owner: Your username
- Space Name: `llm-app`
- License: `Openrail`
- Select the Space SDK: `Docker`
- Docker Template: `Blank`
- Space Hardware: `CPU basic - 2 vCPU - 16 GB - Free`
- Repo type: `Public`

<p align = "center" draggable=”false”>
<img src="https://github.com/AI-Maker-Space/LLMOps-Dev-101/assets/37101144/8f16afd1-6b46-4d9f-b642-8fefe355c5c9"> 
</p>

3. You should see something like this. We're now ready to send our files to our Huggingface Space. After cloning, move your files to this repo and push it along with your docker file. You DO NOT need to create a Dockerfile. Make sure NOT TO push your `.env` file. This should automatically be ignored.

<p align = "center" draggable=”false”>
<img src="https://github.com/AI-Maker-Space/LLMOps-Dev-101/assets/37101144/cbf366e2-7613-4223-932a-72c67a73f9c6"> 
</p>

4. After pushing all files, navigate to the settings in the top right to add your OpenAI API key.

<p align = "center" draggable=”false”>
<img src="https://github.com/AI-Maker-Space/LLMOps-Dev-101/assets/37101144/a1123a6f-abdd-4f76-bea4-39acf9928762"> 
</p>

5. Scroll down to `Variables and secrets` and click on `New secret` on the top right.

<p align = "center" draggable=”false”>
<img src="https://github.com/AI-Maker-Space/LLMOps-Dev-101/assets/37101144/a8a4a25d-752b-4036-b572-93381370c2db"> 
</p>

6. Set the name to `OPENAI_API_KEY` and add your OpenAI key under `Value`. Click save.

<p align = "center" draggable=”false”>
<img src="https://github.com/AI-Maker-Space/LLMOps-Dev-101/assets/37101144/0a897538-1779-48ff-bcb4-486af30f7a14"> 
</p>

7. To ensure your key is being used, we recommend you `Restart this Space`.

<p align = "center" draggable=”false”>
<img src="https://github.com/AI-Maker-Space/LLMOps-Dev-101/assets/37101144/fb1d83af-6ebe-4676-8bf5-b6d88f07c583"> 
</p>

8. Congratulations! You just deployed your first LLM! 🚀🚀🚀 Get on linkedin and post your results and experience! Make sure to tag us at #AIMakerspace !

Here's a template to get your post started!

```
🚀🎉 Exciting News! 🎉🚀

🏗️ Today, I'm thrilled to announce that I've successfully built and shipped my first-ever LLM using the powerful combination of Chainlit, Docker, and the OpenAI API! 🖥️

Check it out 👇
[LINK TO APP]

A big shoutout to the @**AI Makerspace** for all making this possible. Couldn't have done it without the incredible community there. 🤗🙏

Looking forward to building with the community! 🙌✨ Here's to many more creations ahead! 🥂🎉

Who else is diving into the world of AI? Let's connect! 🌐💡

#FirstLLM #Chainlit #Docker #OpenAI #AIMakerspace
```

</details>

<p></p>

### That's it for now!  And so it begins.... :)
>>>>>>> BCBranch
=======
# 🧑‍💻 What is [AI Engineering](https://maven.com/aimakerspace/ai-eng-bootcamp)?

AI Engineering refers to the industry-relevant skills that data science and engineering teams need to successfully **build, deploy, operate, and improve Large Language Model (LLM) applications in production environments**.  

In practice, this requires understanding both prototyping and production deployments.

During the *prototyping* phase, Prompt Engineering, Retrieval Augmented Generation (RAG), Agents, and Fine-Tuning are all necessary tools to be able to understand and leverage. Prototyping includes:
1. Building RAG Applications
2. Building with Agent and Multi-Agent Frameworks
3. Fine-Tuning LLMs & Embedding Models
4. Deploying LLM Prototype Applications to Users

When *productionizing* LLM application prototypes, there are many important aspects ensuring helpful, harmless, honest, reliable, and scalable solutions for your customers or stakeholders. Productionizing includes:
1. Evaluating RAG and Agent Applications
2. Improving Search and Retrieval Pipelines for Production
3. Monitoring Production KPIs for LLM Applications
4. Setting up Inference Servers for LLMs and Embedding Models
5. Building LLM Applications with Scalable, Production-Grade Components

This bootcamp builds on our two previous courses, [LLM Engineering](https://maven.com/aimakerspace/llm-engineering) and [LLM Operations](https://maven.com/aimakerspace/llmops) 👇

- Large Language Model Engineering (LLM Engineering) refers to the emerging best-practices and tools for pretraining, post-training, and optimizing LLMs prior to production deployment.  Pre- and post-training techniques include unsupervised pretraining, supervised fine-tuning, alignment, model merging, distillation, quantization. and others.
    
- Large Language Model Ops (LLM Ops, or LLMOps (as from [WandB](https://docs.wandb.ai/guides/prompts) and [a16z](https://a16z.com/emerging-architectures-for-llm-applications/))) refers to the emerging best-practices, tooling, and improvement processes used to manage production LLM applications throughout the AI product lifecycle.  LLM Ops is a subset of Machine Learning Operations (MLOps) that focuses on LLM-specific infrastructure and ops capabilities required to build, deploy, monitor, and scale complex LLM applications in production environments.  _This term is being used much less in industry these days._

# 🏆 **Grading and Certification**

To become **AI-Makerspace Certified**, which will open you up to additional opportunities for full and part-time work within our community and network, you must:

1. Complete all project assignments.
2. Complete a project and present during Demo Day.
3. Receive at least an 85% total grade in the course.

If you do not complete all assignments, participate in Demo Day, or maintain a high-quality standard of work, you may still be eligible for a *certificate of completion* if you miss no more than 2 live sessions.

# 📚 About

This GitHub repository is your gateway to mastering the art of AI Engineering.  ***All assignments for the course will be released here for your building, shipping, and sharing adventures!***

# 🙏 Contributions

We believe in the power of collaboration. Contributions, ideas, and feedback are highly encouraged! Let's build the ultimate resource for AI Engineering together.

Please to reach out with any questions or suggestions. 

Happy coding! 🚀🚀🚀

>>>>>>> 3cc092a2ce2707bf28c27cb3c1e48e6326463a84
