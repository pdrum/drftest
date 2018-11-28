{% load doc_filters %}

# {{ app_name }}

{{ app_name }} app has the following tests.
Tests are categorized into classes where each class has
several test cases.

{% for class_name, class_docs in app_docs.items %}
## {{ class_name }}

{% if class_docs.description %}
{{ class_docs.description }}
{% endif %}

This class has the following test cases:


{% for method_doc in class_docs.tests %}
<details>
<summary>{% if method_doc.success %}&#10004;{% else %}&#10008;{% endif %} **{{ method_doc.meta.method_name }}**
</summary>

{% if method_doc.meta.docs %}
* **Description:** {{ method_doc.meta.docs }}
{% endif %}
* **URL:** `{{ method_doc.url }}`
* **Method:** `{{method_doc.method}}`
* **Format:** `{{method_doc.format}}`

{% if method_doc.url_kwargs %}
* **Path parameters:** 
```json
{{ method_doc.url_kwargs|to_json }}
```
{% endif %}

{% if method_doc.headers %}
* **Headers:** 
```json
{{ method_doc.headers|to_json }}
```
{% endif %}

{% if method_doc.data %}
* **Request data:** 
```json
{{ method_doc.data|to_json }}
```
{% endif %}

* **Response status code**: {{ method_doc.response.status }}

{% if method_doc.response.data %}
* **Response data:** 
```json
{{ method_doc.response.data|to_json }}
```
{% endif %}

</details>
{% endfor %}

{% endfor %}
