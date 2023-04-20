# ckanext-msl_ckan_util

This extension contains a set of possibly reusable plugins developed for the EPOS MSL CKAN portal.

Plugins contained in this extension:

* msl_custom_facets
* msl_repeating_fields
* msl_search

## Requirements

This extension has been developed and tested with CKAN version 2.9.* 
Use of this extension is depended on the CKAN scheming extension being loaded. 

## Installation of extension

To install ckanext-msl_ckan_util:

1. Activate your CKAN virtual environment, for example:

     . /usr/lib/ckan/default/bin/activate

2. Clone the source and install it on the virtualenv

    git clone https://git.science.uu.nl/epos-msl/msl_ckan_util.git
    cd ckanext-msl_ckan_util
    pip install -e .
	pip install -r requirements.txt

3. Add names of plugins to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`). Specific names and settings per plugin are described in the section of the plugins.

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:

     sudo service apache2 reload


## Config settings

When config settings are required they are described per plugin.

## Custom facets plugin
The custom facets plugin enables easy configuring of displayed facets in plugin by supplying a configuration json file.
A default facet list should be given and optional facet lists per specific package type (configured in CKAN scheming) 
can be configured.

### activate plugin
To activate this plugin add the name `msl_custom_facets` to the `ckan.plugin` setting in the `ckan.ini`.

### config
This plugin requires a json config file to function. The location of the config file must be set in the `ckan.ini` file.
The setting that should be added: `mslfacets.dataset_config` the value should contain the reference to the config 
file. The value should be formatted like `<ckan_extension_name>:<path><filename>`. To reference the sample file config 
supplied with this extension use: `ckanext.msl_ckan_util:samples/facets.json`.

Sample json config file:

     {
     "default":
     {
       "dataset_type": "Type",
       "organization":  "Organizations",
       "groups": "Groups"
     },
     "rockphysics" :
     {
       "msl_material": "Materials",
       "tags": "Tags",
       "msl_rock_measured_property": "Measured property"
     } 

The default key should always be given. A list of facets can be supplied. The keys contain the fields that should be 
faceted on and the value contains the displayed label at the text. Other lists of facets can be configured to be displayed 
for specific dataset types. These should be configured using ckan scheming.

### default CKAN facets

The default implemented CKAN facets are:

      "organization": "Organizations",
      "groups": "Groups",
      "tags": "Tags",
      "res_format": "Formats",
      "license_id": "Licenses"

## Repeating fields plugin

This plugin 'flattens' repeating subfields defined in scheming schemas to enable solr to index the field.

### activate plugin

To activate this plugin add the name `msl_repeating_fields` to the `ckan.plugin` setting in the `ckan.ini`.

### config

This plugin requires a json config file to function. The location of the config file must be set in the `ckan.ini` file.
The setting that should be added: `mslindexfield.field_config` the value should contain the reference to the config
file. The value should be formatted like `<ckan_extension_name>:<path><filename>`. To reference the sample file config 
supplied with this extension use: `ckanext.msl_ckan_util:samples/msl_index_fields.json`.

Sample json config file:

      {
      "special_index_fields": [
        "msl_material",
        "msl_rock_measured_property"
      ]
      }

The `special_index_fields` should contain a list of fields that should be 'flattened' for SOLR indexing.

## Search plugin

This plugin changes all searches to use the SOLR eDisMax query parser instead of the dismax version.

### activate plugin

To activate this plugin add the name `msl_search` to the `ckan.plugin` setting in the `ckan.ini`.


## Developer installation

To install ckanext-msl_ckan_util for development, activate your CKAN virtualenv and
do:

    git clone https://git.science.uu.nl/epos-msl/msl_ckan_util.git
    cd ckanext-msl_ckan_util
    python setup.py develop
    pip install -r dev-requirements.txt


## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini


## Releasing a new version of ckanext-msl_ckan_util

If ckanext-msl_ckan_util should be available on PyPI you can follow these steps to publish a new version:

1. Update the version number in the `setup.py` file. See [PEP 440](http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers) for how to choose version numbers.

2. Make sure you have the latest version of necessary packages:

    pip install --upgrade setuptools wheel twine

3. Create a source and binary distributions of the new version:

       python setup.py sdist bdist_wheel && twine check dist/*

   Fix any errors you get.

4. Upload the source distribution to PyPI:

       twine upload dist/*

5. Commit any outstanding changes:

       git commit -a
       git push

6. Tag the new release of the project on GitHub with the version number from
   the `setup.py` file. For example if the version number in `setup.py` is
   0.0.1 then do:

       git tag 0.0.1
       git push --tags

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
