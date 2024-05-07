From https://www.autismbc.ca/blog/resource-guide/pathological-demand-avoidance-pda-explained/

> Pathological Demand Avoidance (PDA) is an autistic profile. PDA individuals share autistic characteristics and also have many of the ‘key features’ of a PDA profile. It is most widely recognized in the UK. PDA is best explained as an extreme avoidance of everyday activities, refusal of demands and challenges with authority due to severe anxiety. In the United States and Canada, PDA is still emerging and not widely diagnosed by professionals due to lack of awareness.

This streamlit app helps you rephrase your language for effectively communicating with kids with PDA.

Setup
---

You need groq, dotenv and streamlit for python, so install it:
```sh
$ pip install streamlit groq dotenv
```

Add your groq api key. Groq is very fast, and free at the time writing this.
```sh
$ cp .env.template .env
$ vim .env
```

```.env
GROQ_SECRET_ACCESS_KEY=your-key-goes-here
```

Now run the app:
```
$ streamlit run pda.py
```

