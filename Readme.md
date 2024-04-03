## CVapp the job 

Why even creating an app? Because it was my dream for a very long time to make an app. I was even drawing my own platform games in elementary school but was never able to make one! Main goal of this app is to learn python and working with databases (data pipelines, transformations, database architecture).

This project is made to make my life easier and save myself a lot of tedious manual work when looking for a job and to have better feedback and understanding of my applying strategy and companies’s hiring strategy.

I do like databases and for some time it was enough to just write couple lines of where and when did I apply for a job in excel. Later on I needed more. The frontend part of this project is not my goal, but it is necessary. I have never built an app before, so this poses a whole new set of challenges.

My attitude towards this project is based on how it could look like in an ideal world where I knew everything about making an app. Then I have took the core part which I needed most and started there with what I already knew or at least had an idea how it may be done.

### Why this technology

I wanted this system to be **used across devices**. With this I theoretised to write the app for web with **JavaScript generated by AI**. Later I have been told the **Flet framework** would completely solve this issue for me as I can later deside where the app will be deployed. Therefore I decided for Flet.

With this in mind I needed to store the data somewhere. **Cloud solutions with web app** required to deal with accounts, security etc. which was not in my scope for a near future. Use of **SQlite** or anything similar locally had issue with being able to use this only locally. 

For my **prototype** I needed ready access across devices while being able to get to the database from a phone and edit it manually. That ruled out basically any database system. For simplicity while using a prototype I decided **Excel** would be a solution. It was good in drafting a database and using it manually (to check what data will be needed etc.). It is possible to access data on almost any device (as long as it is on One Drive) and I can directly edit data on a phone. Working with excel files locally solved a problem with handling passwords etc. and it was perfect for a prototype. Plus it is easy to rewrite excel data flow into database flow later when app will have edit mode.

I am well aware **Excel is not a good idea for a database**, yet is perfect for prototyping and ease of change. There is in no near future going to be need for account handling therefore there will be no one to mess with data and data structure.

### Prototype

To my surprise first absolutely most needed was not functionality for "where did I sent my CV", rather "to which position I applied to". I needed to pick all relevant data without the need to write it manually. Calendar was basically just a plus with no big manual labor.

It proved challenging to scrape StartUpJobs, therefore I laid it off for some time (dealing with selenium was complicated stuff) and went for Jobs.cz which was very easy to scrape. Issue was with the actual text offer which was clearly inserted in their system with copy-paste style, as many offers had varying text elements and were scraping with different success rate.

### Purpose of this app

This is a code where I am first using classes and preparing a ground for module use. Therefore my main focus is learn how to use them efficiently and still have working app which could help my needs and help with later data analysis. 

Sole purpose of keeping an eye on all those offers is purely analytical. I want to know when and in which circumstances I have best chances and which technologies are desired in my target field.

It is **not about design and beautiful UI**, even though these things are important to me as well. Currently, design and UX is not even on my priority list as my main learning focus lies in backend.

Plus, if I will ever be able to make this into usable app, it **could help community** a lot.

### Timeline

* 2020 no tracking of where did I sent CV, some notes on paper and a lot of chaos
* 2021 first simple excel file to track
* 2022 excel is being redefined as I need more information
* 2023 simple excel has grown into less simple one with basic analysis

* 2024 January first drafts of an app and its desired use
* 2024 February first drafts of database, tested in excel in real life use
* 2024 March first working script for data scraping