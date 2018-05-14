HH Coding Task
==============

This is Hunted Hive coding task.

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django

The task
========

Summary
-------
Your task is to create a django model that would store any data (based on a priori defined data scheme) and make this model usable across the project (admin integration + simple form view for adding new instances).

Requirements
------------
- django model, say `GenericModel`, that stores any data (proposed aproach is to use JSON field but we're open to better solutions)
- come up with a scheme describing data that `GenericModel` can store/process, for simplicity let's store it as a project-wide setting. Scheme can support only basic data types, like number, strings etc.
- view with form for end users for adding new instances of the `GenericModel` with appropriate validation. Example: if scheme declares we have "age" field that is of "integer" type and "name" field that is of "string" type, the form should contain these 2 fields (inputs). If scheme contains 3 fields of "string" type, the form should contain 3 appropriately named inputs etc. Putting text in the form field will cause validation error with relevant message for end users
- django admin integration so admin can view/edit `GenericModel` instances

How to set up this project?
===========================
The project has been built using cookiecutter-django template (https://github.com/pydanny/cookiecutter-django). Please refer to its docs for some more information. Launching the project follows well known guidelines of setting up a standard django project:

- creating virtualenv
- installing requirements
- running migrations
- running django dev server

Collaboration
=============
Please create a separate branch where you can commit your work. Follow general guidelines of keeping git history clean and use meaningful messages. Once you're done, please create a pull request where you can describe your solution.

Questions
=========
**Q:** In my opinion, the optimal solution, in this case, is the usage of JSONField because JSON support exists in some DBMS, and this fact allows to search by them and additionally it could be easily modified. As an alternative - using at least two models instead of one. The first model to define the object, while the second one is being implemented as key/value with the reference to the object. In the latest case the cons is that we get the entity, that doesn't provide an object in fact. 

**A:** The latter approach (using 2 models) I think it's not the best here, because if a model has lots of fields you'd need fetch lots of models to just have one entity. And if you're going to iterate over let's say 100 objects where each model has 100 fields then you have 10 000 DB reads to just fetch 100 entities.

**Q:** May I use additional solutions like https://marshmallow.readthedocs.io/en/latest/ or http://docs.python-cerberus.org/en/stable/?

**A:** Yep, feel free to use additional solutions and libraries like marshmallow. However not sure if it's not limiting us from having truly generic structure? Marshmallow needs to have Schema class created. Not sure how are you going to have this class working if the schema inside needs to be dynamic (based on configuration)? One way is metaclasses but it's not worth the effort I guess unless you really understsand metaclasses in Python.

**Q:** How is the schema defined? What I mean is your vision of how it should be defined, stored and served? It could be defined by code, like classes as in marshmallow or being stored in a text file next to the code or just be stored in the DB. The decision here strongly depends on the use case and it is not obvious as the task is synthetic. I would recommend marshmallow approach, that will allow solving migration questions, though other approaches are more flexible.

**A:** So how to define the schema is a task itself. It's up to you. Though the readme says:
"come up with a scheme describing data that GenericModel can store/process, for simplicity let's store it as a project-wide setting." so I guess the answer is to store it as a project-wide setting.
Example: python dict that describes fields/types etc.

**Q:** Access to attributes should be like `GenericModelInstance.age`?

**A:**  Doesn't matter, as you wish. Let's not invent new requirements, and keep the task simple. The goal of the task is to:

* Django model that stores any data
* scheme
* view with a working form
* Django admin integration so admin can edit the instances somehow

**Q:** Do we need to support null and/or default values for GenericModel? Should data stored in model be always initialized with a value or necessary to support null, for example for optional settings?

**A:** Good question. For the sake of simplicity let's assume all attributes are optional

**Q:** How to handle changes in the pre-defined schema? Are migrations necessary?

**A:** No, no migrations are necessary. There's only a form for adding new instances, so if the scheme changes, the form for adding new objects should also be changed. But that doesn't touch previously added objects.

**Q:** How should it be displayed for the user and for the admin in the admin panel? From my understanding, there should be an option to edit each field like it is model attribute

**A:** Whatever is most simple and quick. It might look bad in terms of UI but functionally it should be working.

**Q:** Do we need to store the references to other objects?

**A:** Good question. Let's assume "no" for the time being.
