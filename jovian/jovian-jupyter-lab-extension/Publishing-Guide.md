## Guide To Publish the Extension to npm
---

### Before you begin register for a [npm](https://www.npmjs.com/ "npm") account and enable 2FA, and login through the console:

```shell
$ npm login
```

---
### In order to publish the package, you need to have ``` package.json``` file in the directry for npm to create a package.

### <span style="color:red"$*Important note:* </span>

#### Make sure that the `package.json` includes all the dependencies required by the extension and keywords include the following as this will affect the discoverability of the extension in Jupyter Lab :

```json
"keywords": [
    "jupyter",
    "jupyterlab",
    "jupyterlab-extension"
  ]
```
---

#### Once you've verified and made necessary change to the ```package.json``` file, you need to rebuild extension and pack the extension:

```shell
$ jlpm run clean && jlpm run build

$ npm pack
```

#### npm will ask you to verify information in ```package.json```.

#### Now we are ready to publish:

```shell
$ npm publish
```
#### This will ask for login credentials if you have not logged in and it will ask for a 2FA code.

### Done! The package is published and ready to be installed via the Jupyter Lab's Extension Manager or by using the console:

```shell
$ npm i <package-name>
```
OR

```shell
jupyter labextension install jovian-lab-ext-test
```
### Some notes:

- npm package name rules must be followed [npm package naming conventions](https://docs.npmjs.com/files/package.json).
- Once package is published, the name of the package is taken forever it cannot be used by any other package.

### To update the package:
- Once you have made any changes to the extension rebuild the extension and run:

```shell
$ npm version <patch/minor/major>
$ npm pack
$ npm publish
```
- If you have modified dependencies, before you update the package (version number is optional):
```shell
$ npm install <package-name>@'version' --save-prod {this will update the dependencies attribute}
$ npm install <package-name>@'version' --save-dev {this will update the devDependencies attribute}
```