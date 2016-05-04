![](./static/favicon.ico) Hearcloud
============

##About the project

**Heardcloud** is a web application that lets you effortlessly store all your music files and make them availabe anytime and everywhere you want. You can organize your songs inside the platform, editing all their attributes (like title, artists, artwork, ...) and download the updated files again to your system.

![Hearcloud-Home](http://i.imgur.com/ap5PRIt.png)

## Why did I start this project?

Since music is one of my passions, I found that I had a bunch of songs distributed on a wide range of devices  (desktop computer, laptop, hdds, pen drives, smartphone, tablets, etc) which were also in general duplicated. Because of that, I felt I needed something that would let me store all of them in one place where I could also organise my collection, editing their tags and making them available whenever I want to play or download again.

## Why Django?

From all the programming languages that I've studied so far, Python es the one with which I'm feeling more comftable. So, when I found Django, I immediately wanted to learn more about it.

## Requirements

[Here](./requirements.txt) is a list of everything you will need in order to run the project on your machine. But don't worry, if you read the next section, you will find how to install easily.

## How to install

Run:

```
$ git clone https://github.com/mpvillafranca/hearcloud.git
$ cd hearcloud
$ virtualenv hcenv
$ source hcenv/bin/activate
$ cd hearcloud
$ pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py runserver
```

## Some stuff I'm planning to include
- [ ] [jQuery File Upload](https://github.com/blueimp/jQuery-File-Upload): to allow users upload multiple file songs at the same time.

- [ ] [Mixbolt](https://github.com/adaline/mixbolt): I'm trying to figure out how to include this project as my music player, refactoring the code to get the appearance of a single deck instead of a complete DJ mixer.

## License

All the code developed for the Headcloud project is licensed under GNU AFFERO GENERAL PUBLIC LICENSE Version 3. You can check the license terms [here](./LICENSE).

## Resources

Everything related to the third party code that this project use goes here...
