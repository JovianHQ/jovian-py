define([
  "jquery",
  "base/js/namespace",
  "base/js/dialog",
  "base/js/keyboard"
], function ($, Jupyter, dialog, keyboard) {
  /**
   * create boolean variable: sidebar_open
   * and initiate it to false, because at the beginning
   * the sidebar is close.
   */
  var sidebar_open = { value: false };
  const nbName = Jupyter.notebook.notebook_name;

  const get_version_list_url = () => {
    /**
     * promise function: to get
     * the list of urls, for every
     * version of the current
     * notebook.
     */

    return new Promise(resolve => {
      const valStatus = data => {
        resolve(data.content.text.trim());
      };

      const versionsUrls = `
  from jovian.utils.api import get_gist
  from jovian.utils.credentials import read_webapp_url
  from jovian.utils.misc import urljoin
  import json
  
  with open('.jovianrc') as f:
      jovianrc = json.load(f)
  
  slug = jovianrc['notebooks']["${nbName}"]['slug']
  gist_metadata = get_gist(slug)
  username = gist_metadata['currentUser']['username']
  title = gist_metadata['title']
  count = gist_metadata['version']
  
  link = urljoin(read_webapp_url(), username, title)
  version_urls = [urljoin(link, str(version)) for version in range(1, count+1)]
      
  print(versions_urls)`;

      Jupyter.notebook.kernel.execute(versionsUrls, {
        iopub: { output: valStatus }
      });
    });
  };

  const get_version_list = () => {
    /**
     * promise function: to get the
     * list of versions, that
     * belong to the current notebook
     */

    return new Promise(resolve => {
      const valStatus = data => {
        resolve(data.content.text.trim());
      };

      const versionNames = `
  from jovian.utils.api import get_gist
  import json
  
  with open('.jovianrc') as f:
      jovianrc = json.load(f)
  
  slug = jovianrc['notebooks']["${nbName}"]['slug']
  gist_metadata = get_gist(slug)
  
  version_names = [version['title'] for version in gist_metadata['versions']]
  
  print(version_names)`;

      Jupyter.notebook.kernel.execute(versionNames, {
        iopub: { output: valStatus }
      });
    });
  };

  const get_avatars = () => {
    /**
     * promise function: to get
     * the list of avatars, that
     * belong to the current notebook
     */

    return new Promise(resolve => {
      const valStatus = data => {
        resolve(data.content.text.trim());
      };

      const avatars = `
  from jovian.utils.api import get_gist
  import json
  
  with open('.jovianrc') as f:
      jovianrc = json.load(f)
  
  slug = jovianrc['notebooks']["${nbName}"]['slug']
  gist_metadata = get_gist(slug)
  
  avatar_list = [collaborator['account']['avatar'] for collaborator in gist_metadata['members']]
  print(avatar_list)`;

      Jupyter.notebook.kernel.execute(avatars, {
        iopub: { output: valStatus }
      });
    });
  };

  const get_colab_names = () => {
    /**
     * promise function: to get
     * the list of names of the
     * collaborators, to the
     * current notebook.
     */

    return new Promise(resolve => {
      const valStatus = data => {
        resolve(data.content.text.trim());
      };

      const c_names = `
  from jovian.utils.api import get_gist
  import json
  
  with open('.jovianrc') as f:
      jovianrc = json.load(f)
  
  slug = jovianrc['notebooks']["${nbName}"]['slug']
  gist_metadata = get_gist(slug)
  
  collaborator_names = [collaborator['account']['name'] for collaborator in gist_metadata['members']]
  
  print(collaborator_names)`;

      Jupyter.notebook.kernel.execute(c_names, {
        iopub: { output: valStatus }
      });
    });
  };

  const get_latest_version = () => {
    /**
     * promise fuction: to get
     * the latest version number of
     * the current notebook
     */

    return new Promise(resolve => {
      const valStatus = data => {
        resolve(data.content.text.trim());
      };

      const listV = `
  from jovian.utils.api import get_gist
  import json
  
  with open('.jovianrc') as f:
      jovianrc = json.load(f)
  
  slug = jovianrc['notebooks']["${nbName}"]['slug']
  gist_metadata = get_gist(slug)
  
  print(json.dumps(gist_metadata))`;
      console.log(listV);
      Jupyter.notebook.kernel.execute(listV, {
        iopub: { output: valStatus }
      });
    });
  };

  const get_url = () => {
    /**
     * promise function: to get
     * the url to the current notebook
     * this url will be use for
     * share dialog.
     */

    return new Promise(resolve => {
      const valStatus = data => {
        resolve(data.content.text.trim());
      };

      const rc = `
  from jovian.utils.credentials import read_webapp_url
  import json
  
  with open('.jovianrc') as f:
      jovianrc = json.load(f)
  
  slug = jovianrc['notebooks']["${nbName}"]['slug']
  gist_metadata = get_gist(slug)
  username = gist_metadata['currentUser']['username']
  title = gist_metadata['title']
  
  print(urljoin(read_webapp_url(), username, title))`;
      console.log(rc);
      Jupyter.notebook.kernel.execute(rc, {
        iopub: { output: valStatus }
      });
    });
  };

  async function user_and_notebook() {
    /**
     * This function will be
     * used to display the user
     * name and current
     * notebook name.
     */

    let list = "";
    await get_latest_version().then(theList => {
      list = theList;
    });
    let new_list = JSON.parse(list);

    let user_name = new_list.currentUser.username;
    let display = user_name + " / " + new_list.title;
    console.log("user_and_notebook", display);
    document.getElementById("prototypeONe").innerHTML = display;
  }

  async function refresh_latest_version() {
    /**
     * This function updates the
     * latest vesion number for
     * current notebook
     */

    let list = "";
    await get_latest_version().then(theList => {
      list = theList;
    });
    let version_number = JSON.parse(list);

    let new_latestVersion = "Version " + version_number.version;
    console.log("refresh_latest_version", new_latestVersion);
    document.getElementById("prototypeTwo").innerHTML = new_latestVersion;
  }

  async function refresh_version_control() {
    /**
     * This function updates the
     * version control dropdown menu
     */

    let list1 = "";
    await get_version_list_url().then(theList => {
      list1 = theList;
    });
    var links = list1.split(", ");

    let list2 = "";
    await get_version_list().then(theList2 => {
      list2 = theList2;
    });
    var versions = list2.split(", ");
    console.log("refresh_latest_version_control", links, versions);
    let new_html =
      '<!DOCTYPE html><html><head><meta charset="utf-8"> <style type="text/css">select{font-size: 400%;}</style></head><body><center><form size="50" name="jump2"><select id="container" name="myjumpbox" OnChange="window.open(jump2.myjumpbox.options[selectedIndex].value)"></select></form></center><script>arr = ' +
      versions +
      " ;link = " +
      links +
      ' ;arr.forEach((num1,index)=>{const num2 = link[index];let card = document.createElement("div");var option = document.createElement("OPTION");option.setAttribute("value",link[index]);txt = document.createTextNode(arr[index]);option.appendChild(txt);card.insertBefore(option,card.lastChild);let container = document.querySelector("#container");container.appendChild(option);});</script></body></html>';
    console.log("refresh_latest_version_control", new_html);
    document.getElementById("prototypeThree").src =
      "data:text/html;charset=utf-8," + encodeURI(new_html);
  }

  async function share_dialog() {
    /**
     * This function display
     * buttons for the share dialog
     * module
     */

    let url = "";
    await get_url().then(theUrl => {
      url = theUrl;
    });

    var facebook =
      '<div id="fb-root"></div><script async defer crossorigin="anonymous" src="https://connect.facebook.net/en_US/sdk.js#xfbml=1&version=v6.0"></script><div class="fb-share-button" data-href=' +
      url +
      ' data-layout="button_count" data-size="large"><a target="_blank" href="https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fdevelopers.facebook.com%2Fdocs%2Fplugins%2F&amp;src=sdkpreparse" class="fb-xfbml-parse-ignore">Share</a></div>';
    var twitter =
      '<div><a class="twitter-share-button" href="https://twitter.com/intent/tweet" data-size="large" data-text="custom text" data-url=' +
      url +
      ' data-hashtags="" data-via="" data-related="twitterapi,twitter">Tweet</a><script>window.twttr = (function(d, s, id) { var js, fjs = d.getElementsByTagName(s)[0], t = window.twttr || {}; if (d.getElementById(id)) return t; js = d.createElement(s); js.id = id; js.src = "https://platform.twitter.com/widgets.js"; fjs.parentNode.insertBefore(js, fjs); t._e = []; t.ready = function(f) { t._e.push(f);}; return t;} (document, "script", "twitter-wjs"));</script></div>';
    var linkedin =
      "<div><script src='https://platform.linkedin.com/in.js' type='text/javascript'>lang: en_US</script><script type='IN/Share' data-url='" +
      url +
      "'></script></div>";
    let new_html =
      "<html><body><center><table><tr><th>" +
      facebook +
      "</th><th>" +
      twitter +
      "</th></tr></table></center><br><h><center>" +
      linkedin +
      "</center></h></body></html>";

    document.getElementById("prototypeFour").src =
      "data:text/html;charset=utf-8," + encodeURI(new_html);
  }

  async function collaborators() {
    /**
     * This function
     * will be use to
     * display collaborators
     */

    let avatar_list = "";
    await get_avatars().then(List => {
      avatar_list = List;
    });
    var avatars = avatar_list.split(", ");

    let avatar_names = "";
    await get_colab_names().then(List2 => {
      avatar_names = List2;
    });
    var fullname = avatar_names.split(", ");

    var n = fullname.length;

    var new_html =
      '<!DOCTYPE html><html><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css"><body><center><b><h style="color:#585858";>Collaborators: ' +
      n +
      '</h></b></center><div class="w3-card-4 w3-margin" style="width:100%"><div class="w3-xlarge w3-display-bottomleft w3-padding"></div></div><div class="w3-row"><div id="container"></div></div><script>arr = ' +
      fullname +
      ";links = " +
      avatars +
      ';arr.forEach((num1,index) => {const num2 = links[index];let card = document.createElement("card");card.setAttribute("class","w3-third w3-center");let h3 = document.createElement("h3");h3.style.color = "#585858";txt = document.createTextNode(arr[index]);h3.appendChild(txt);card.insertBefore(h3,card.lastChild);let avatar = document.createElement("IMG");avatar.setAttribute("src",links[index]);avatar.setAttribute("alt","sun");avatar.setAttribute("width","80px");card.appendChild(avatar);let container = document.querySelector("#container");container.appendChild(card);});</script></body></html>';

    document.getElementById("prototypeFive").src =
      "data:text/html;charset=utf-8," + encodeURI(new_html);
  }

  function loadJovianExtension() {
    /**
     *  Jupyter extension to commit the notebook to Jovian.
     *
     *  Commits the notebook if there is a valid API key available
     *  else prompts the user with a modal to get the API key.
     */

    var saveFail = false;
    //config
    const settingsFeature = false;
    const sidebarFeature = false;

    const setCurrentSlug = () => {
      const filename = Jupyter.notebook.notebook_name;
      const code = `
from jovian.utils.rcfile import get_notebook_slug
get_notebook_slug("${filename}")
import jovian
jovian.utils.jupyter.get_notebook_name_saved = lambda: "${filename}"      
`;


      Jupyter.notebook.kernel.execute(code);
    };
    Jupyter.notebook.events.on("kernel_ready.Kernel", () => {
      // Extension only loads up when there is browser reload, this ensures both when kernel is restarted and that kernel is ready
      setCurrentSlug();
    });

    const jvnCommit = () =>
      /**
       * Commits the notebook to Jovian(https://jovian.ai).
       *
       * Returns:
       *  - Committed notebook's link: for successful commit
       *  - last line logged: for any other case
       *
       * Python code uses:
       *  - jovian.commit()
       */

      new Promise(resolve => {
        const jvnLog = data => {
          resolve(data.content.text.trim());
        };

        let filename = Jupyter.notebook.notebook_name.split(".");
        filename.pop();
        filename.join();
        let commit = `commit(filename=${getValInPython(filename)})`;

        // if we have a set of params already, then use it to call commit.
        if ((params = getParams()) != null) {
          const new_project = params.new_project;
          const git_commit = params.git_commit;
          const files = getArrayInPython(params.files);
          const outputs = getArrayInPython(params.outputs);
          const privacy = getValInPython(params.privacy);
          const environment = getValInPython(params.environment);
          const project_id = getValInPython(params.project_id);
          const message = getValInPython(params.message);
          const git_message = getValInPython(params.git_message);

          commit =
            "commit(" +
            "filename=" +
            getValInPython(filename) +
            ",message=" +
            message +
            ",git_commit=" +
            git_commit +
            ",git_message=" +
            git_message +
            ",privacy=" +
            privacy +
            ",new_project=" +
            new_project +
            ",files=" +
            files +
            ",project=" +
            project_id +
            ",outputs=" +
            outputs +
            ",environment=" +
            environment +
            ")";
        }

        const jvn_commit = `
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
import json

jvn_update = StringIO()

with redirect_stdout(jvn_update):
  from jovian import commit

jvn_f_out = StringIO()
jvn_f_err = StringIO()

with redirect_stdout(jvn_f_out), redirect_stderr(jvn_f_err):
  jvn_msg = ${commit}

print(json.dumps({'msg': jvn_msg, 'err': jvn_f_err.getvalue(), 'update': jvn_update.getvalue()}))

del jvn_update, jvn_f_out, jvn_f_err, jvn_msg`;

        /* Saves the notebook creates a checkpoint and then commits*/
        Jupyter.notebook.save_checkpoint();
        Jupyter.notebook.events.one("notebook_saved.Notebook", function () {
          Jupyter.notebook.kernel.execute(jvn_commit, {
            iopub: { output: jvnLog }
          });
        });
        Jupyter.notebook.events.one(
          "notebook_save_failed.Notebook",
          function () {
            saveFail = true;
            Jupyter.notebook.kernel.execute(jvn_commit, {
              iopub: { output: jvnLog }
            });
          }
        );
      });

    const validateApi = () =>
      /**
       * Validates the stored/entered API key.
       *
       * Returns:
       *   - "valid"   : valid key ready for commit
       *   - "invalid" : invalid/expired key
       *   - "nil"     : credentials not found (new user or creds are deleted)
       *
       * Python code uses
       *   - jovian.utils.credentials.validate_api_key
       *   - jovian.utils.credentials.read_api_key_opt
       *   - jovian.utils.credentials.creds_exist
       */

      new Promise(resolve => {
        const valStatus = data => {
          resolve(data.content.text.trim());
        };

        const validate_api =
          "from jovian.utils.credentials import validate_api_key\n" +
          "from jovian.utils.credentials import read_api_key_opt, creds_exist\n" +
          "key_status = 'nil'\n" +
          "if creds_exist():\n" +
          "\tcurrent_key, _ = read_api_key_opt()\n" +
          "\tif(validate_api_key(current_key)):\n" +
          '\t\tkey_status = "valid"\n' +
          "\telse:\n" +
          '\t\tkey_status = "invalid"\n' +
          "print(key_status)\n";

        Jupyter.notebook.kernel.execute(validate_api, {
          iopub: {
            output: valStatus
          }
        });
      });

    function updateForm(jvn_modal, shown = false) {
      /**
       * Updates the form layout.
       *
       * Validates the API key and updates the layout based on the state of the key.
       *  - valid   : Triggers jvnCommit(), presents the modal with information from jvnCommit()
       *  - invalid : Form with a error message and input box(glow in red).
       *  - nil     : Form with a input box(glow in blue).
       *
       * Params:
       *  - jvn_modal : reference to jQuery modal object.
       *  - shown     :
       *    - true  : Triggered from a modal(modal already shown).
       *    - false : Triggered from the toolbar button(modal not shown).
       */

      const val = validateApi().then(key_status => {
        if (key_status === "valid") {
          jvn_modal.find("#save_button").hide();
          jvn_modal.find("#text_box").hide();

          if (!shown) {
            jvn_notif.element.show(); // show "committing to jovian..." on the menubar

            jvnCommit().then(log_data => {
              const output = JSON.parse(log_data);
              const msg = output["msg"];
              const err = output["err"];
              const update = output["update"];

              function copyToClipboard() {
                jvn_modal.find("#i_label").append($("<textarea>").val(msg)); // temp element
                jvn_modal.find("textarea").select(); // select the text as required by execCommand
                document.execCommand("copy");
                jvn_modal.find("textarea").remove();

                // update the copy button and disable it
                jvn_modal
                  .find("#copy")
                  .text("Copied")
                  .removeClass("btn-primary")
                  .addClass("btn-success")
                  .attr("disabled", true);
              }

              // Successful Commit
              if (msg) {
                const nb_link = $("<a/>")
                  .attr("href", msg)
                  .attr("target", "_blank")
                  .text(msg);

                const copy_btn = $("<button/>")
                  .attr("id", "copy")
                  .attr("type", "button")
                  .css("margin-left", "5px")
                  .css("line-height", "15px")
                  .click(copyToClipboard)
                  .text("Copy")
                  .addClass("btn-primary");

                jvn_modal
                  .find("#i_label")
                  .text("Committed Successfully  ")
                  .append(
                    $(
                      '<i class="fa fa-check-circle" aria-hidden="true"></i>'
                    ).css("color", "green")
                  )
                  .append($("<br/>"))
                  .append(nb_link)
                  .append(copy_btn);

                if (err) {
                  const label = $("<p/>")
                    .text("Warning ")
                    .append(
                      $(
                        '<i class="fa fa-exclamation-triangle" aria-hidden="true"></i>'
                      ).css("color", "rgb(191, 191, 0)")
                    );
                  const p = $("<p/>").text(err);
                  jvn_modal
                    .find("#i_label")
                    .append($("<br/>"))
                    .append($("<br/>"))
                    .append(label)
                    .append(p);
                }

                if (saveFail) {
                  const label = $("<p/>")
                    .text("Auto Save failed ")
                    .append(
                      $(
                        '<i class="fa fa-exclamation-triangle" aria-hidden="true"></i>'
                      ).css("color", "rgb(191, 191, 0)")
                    );
                  const p = $("<p/>").text(
                    "Committed contents might not be up to date. Please save the notebook manually and commit again."
                  );
                  jvn_modal
                    .find("#i_label")
                    .append($("<br/>"))
                    .append($("<br/>"))
                    .append(label)
                    .append(p);
                  saveFail = false;
                }
                if (sidebarFeature) {
                  user_and_notebook();
                  refresh_latest_version();
                  refresh_version_control();
                  share_dialog();
                  collaborators();
                }
              } else {
                jvn_modal
                  .find("#i_label")
                  .text("Commit failed ")
                  .append(
                    $('<i class="fa fa-times" aria-hidden="true"></i>').css(
                      "color",
                      "red"
                    )
                  );

                if (err) {
                  const p = $("<p/>").text(err);
                  jvn_modal.find("#i_label").append(p);
                }
              }

              if (update) {
                const label = $("<p/>").text("Update Available");
                const p = $("<p/>").text(update);

                jvn_modal.find("#i_label").append(label).append(p);
              }

              jvn_notif.element.hide(); // hide "Committing to Jovian..."
              jvn_modal.modal("show");
            });
          } else {
            // when user entered and valid key
            return "saved_valid_key";
          }
        } else if (key_status === "invalid") {
          // show error message and make the glow red
          jvn_modal.find("#text_box").val("");
          jvn_modal.find("#input_div").addClass("has-error");
          jvn_modal.find("#e_label").show();
          jvn_modal.find("#save_button").show();

          if (!shown) {
            jvn_modal.modal("show");
          }
        } else {
          if (!shown) {
            jvn_modal.modal("show");
          }
        }
      });
      return val;
    }

    const formUI = function () {
      /**
       * Body of the Form
       *
       * Layout:
       *  - form : class: form-horizontal
       *    - div :
       *      - label : id: i_label | text: Please enter your API key from [Jovian](https://jovian.ai)
       *      - input : id: text_box | class: form-control | placeholder: {default_text}
       *      - label : id: e_label | text: Invalid API key | hidden: by default
       *
       */
      const form = $("<form/>").addClass("form-horizontal");

      const div = $("<div/>").attr("id", "input_div").appendTo(form);

      const help_label = $("<label/>")
        .attr("id", "i_label")
        .text("Please enter your API key from Jovian");
      // TODO: Configure correct WEBAPP_URL
      // .append(
      //   $("<a/>")
      //     .attr("href", "https://jovian.ai?utm_source=nb-ext")
      //     .attr("target", "_blank")
      //     .text("Jovian")
      // );

      const input_box = $("<input/>")
        .addClass("form-control")
        .attr("id", "text_box")
        .attr("type", "password")
        .attr("placeholder", "Paste and Save your API key");

      const error_msg = $("<label />")
        .attr("id", "e_label")
        .css("color", "red")
        .text("Invalid API key")
        .hide();

      div.append(help_label).append(input_box).append(error_msg);

      input_box.bind("keyup paste", function () {
        error_msg.hide();
        div.removeClass("has-error");
      });

      return form;
    };

    const modalInit = function () {
      /**
       * Initializes a dialog modal triggered by the button on the toolbar
       *
       * Body: formUI()
       *
       * Button:
       *  - Save   : Uses jovian.utils.credentials.write_api_key to save the API key from #text_box
       *             id: save_button | class: btn-primary
       */
      const jvn_modal = dialog.modal({
        show: false,
        title: "Commit to Jovian",
        body: formUI,
        notebook: Jupyter.notebook,
        keyboard_manager: Jupyter.notebook.keyboard_manager,
        buttons: {
          Save: {
            id: "save_button",
            class: "btn-primary",
            click: function () {
              const api_key = $("#text_box").val();
              const write_api =
                "from jovian.utils.credentials import write_api_key\n" +
                "write_api_key('" +
                api_key +
                "')\n";

              Jupyter.notebook.kernel.execute(write_api);
              jvn_modal.data("bs.modal").isShown = false; // Retains the modal

              updateForm(jvn_modal, true).then(x => {
                jvn_modal.data("bs.modal").isShown = true; // Modal can be dismissed after this

                if (x == "saved_valid_key") {
                  jvn_modal.find(".close").click();
                  alert(
                    "API key verified and saved. Please press the 'Commit' button again."
                  );
                }
              });
            }
          }
        },
        open: function () {
          // bind enter key for #save_button when the modal is open
          jvn_modal.find("#text_box").keydown(function (event) {
            if (event.which === keyboard.keycodes.enter) {
              jvn_modal.find("#save_button").first().click();
              return false;
            }
          });

          // Select the input when modal is open, easy to paste the key without the need for user to click first
          jvn_modal.find("#text_box").focus().select();
        }
      });

      updateForm(jvn_modal);
    };

    const formParamsUI = function () {
      /**
       * Body of the Form
       *
       * Layout:
       *  - form : class: form-horizontal
       *    - div :
       *      - 10 x div :
       *        - label : text: the description of each parameter
       *        - input or selection
       *          | input : the text box for collecting parameters' value
       *          | selection: a list of values for users to pick for parameters
       *
       */
      const form = $("<form/>").addClass("form-horizontal");

      const div = $("<div/>").attr("id", "input_div").appendTo(form);

      const message = $("<div/>")
        .append($("<label/>").text("Version Title"))
        .append(
          $("<input/>")
            .addClass("form-control")
            .attr("id", "project_msg_box")
            .attr("placeholder", "The title for this version")
        )
        .append("<br>");

      const filename = $("<div/>")
        .append($("<label/>").text("Jupyter Notebook - file name"))
        .append(
          $("<input/>")
            .addClass("form-control")
            .attr("id", "nb_filename_box")
            .val(Jupyter.notebook.notebook_name.replace(".ipynb", ""))
            .prop("disabled", true)
        )
        .append("<br>");

      const files = $("<div/>")
        .append(
          $("<label/>").text(
            "Additional scripts & utilities (comma separated) e.g helper.py, input.csv"
          )
        )
        .append(
          $("<input/>")
            .addClass("form-control")
            .attr("id", "files_box")
            .attr("placeholder", "utils.py, inputs.csv")
        )
        .append("<br>");

      const environment = $("<div/>")
        .append($("<label/>").text("Python environment type (Anaconda or Pip)"))
        .append(
          $("<select/>")
            .attr("id", "env_opt")
            .addClass("form-control")
            .append($("<option/>").text("auto"))
            .append($("<option/>").text("conda"))
            .append($("<option/>").text("pip"))
            .append($("<option/>").text("None"))
            .css("margin-left", "0em")
        )
        .append("<br>");

      const project_id = $("<div/>")
        .append(
          $("<label/>").text(
            "(optional)Commit to an existing project eg. username/project-title"
          )
        )
        .append(
          $("<input/>").addClass("form-control").attr("id", "project_id_box")
        )
        .append("<br>");

      const new_project = $("<div/>")
        .append(
          $("<label/>").text(
            "Create a new project (instead of updating the existing project)?"
          )
        )
        .append(
          $("<select/>")
            .attr("id", "if_new")
            .addClass("form-control")
            .append($("<option/>").text("True"))
            .append($("<option/>").text("False"))
            .css("margin-left", "0em")
        )
        .append("<br>");

      const privacy = $("<div/>")
        .append(
          $("<label/>").text("Privacy (applicable only for new projects)")
        )
        .append(
          $("<select/>")
            .attr("id", "nb_opt")
            .addClass("form-control")
            .append($("<option/>").text("auto"))
            .append($("<option/>").text("public"))
            .append($("<option/>").text("secret"))
            .append($("<option/>").text("private"))
            .css("margin-left", "0em")
        )
        .append("<br>");

      const outputs = $("<div/>")
        .append(
          $("<label/>").text(
            "Additional outputs or artifacts (comma separated) e.g. model.h5, submission.csv"
          )
        )
        .append(
          $("<input/>")
            .addClass("form-control")
            .attr("id", "artifacts_box")
            .attr("placeholder", "submission.csv, weights.h5")
            .val("")
        )
        .append("<br>");

      const git_commit = $("<div/>")
        .append(
          $("<label/>").text(
            "Perform Git commit (if notebook is in a git repository)"
          )
        )
        .append(
          $("<select/>")
            .attr("id", "if_git")
            .addClass("form-control")
            .append($("<option/>").text("True"))
            .append($("<option/>").text("False"))
            .css("margin-left", "0em")
        )
        .append("<br>");

      const git_message = $("<div/>")
        .append($("<label/>").text("Git commit message"))
        .append(
          $("<input/>")
            .addClass("form-control")
            .attr("id", "git_msg_box")
            .attr("placeholder", "Message for git commit")
        );

      div
        .append(message)
        .append(filename)
        .append(files)
        .append(environment)
        .append(new_project)
        .append(project_id)
        .append(privacy)
        .append(outputs)
        .append(git_commit)
        .append(git_message);

      return form;
    };

    const settingsUI = function () {
      /**
       * Body of the Form
       *
       * Layout:
       *  - div :
       *    - label : text: Set Default Commit Parameters
       *    - input : type: button | id: default_param_button | class: btn btn-primary | text: Set Default | title: Open Parameter Window to set Default Parameters
       *
       *    - label : text: Clear API Key
       *    - input : type: button | id: clear_api_button | class: btn btn-primary | text: Clear Key | title: Clear the Jovian API key
       *
       *    - label : text: Add/Change API Key
       *    - input : type: button | id: change_api_button | class: btn btn-primary | text: Change Key | title: Add/Change the Jovian API key
       *
       *    - label : text: Disable Jovian Extension
       *    - input : type: button | id: disable_button | class: btn btn-primary | text: Disable | title: Disable the Jovian Extension
       *
       */
      const div = $("<div/>").attr("id", "input_div");

      const option_Set_Default = $("<div/>")
        .append(
          $("<label/>").text("Set default options for every jovian commit")
        )
        .append(
          $("<button/>")
            .attr("id", "default_param_button")
            .addClass("btn btn-primary")
            .text("Set Default Parameters")
            .attr("title", "Set options")
        );

      const option_Clear_API = $("<div/>")
        .append($("<label/>").text("Remove the configured Jovian API Key"))
        .append(
          $("<button/>")
            .attr("id", "clear_api_button")
            .addClass("btn btn-primary")
            .text("Clear API key")
            .attr("title", "Clear API Key")
        );

      const option_Change_API = $("<div/>")
        .append($("<label/>").text("Replace the configured API Key"))
        .append(
          $("<button/>")
            .attr("id", "change_api_button")
            .addClass("btn btn-primary")
            .text("Change")
            .attr("title", "Change API Key")
        );

      const option_Disable_Ext = $("<div/>")
        .append($("<label/>").text("Disable the Jovian Extension"))
        .append(
          $("<button/>")
            .attr("id", "disable_button")
            .addClass("btn btn-primary")
            .text("Disable")
            .attr("title", "Disable")
        );

      div
        .append(option_Set_Default)
        .append(option_Clear_API)
        .append(option_Change_API)
        .append(option_Disable_Ext);

      return div;
    };

    const settingsDialog = function () {
      /**
       * Initializes a dialog modal triggered by a dropdown button on the toolbar
       *
       * Body: settingsUI()
       *
       */
      const jvn_setting_modal = dialog.modal({
        show: false,
        title: "Jovian Settings",
        body: settingsUI,
        notebook: Jupyter.notebook,
        keyboard_manager: Jupyter.notebook.keyboard_manager,
        open: function () {
          const option1 = $("#default_param_button");
          const option2 = $("#clear_api_button");
          const option3 = $("#change_api_button");
          const option4 = $("#disable_button");

          option1.click(() => jvn_setting_modal.find(".close").click());
          option1.click(() => openModal(saveParams));
          option2.click(() => clearAPI());
          option3.click(() => changeAPI());
          option4.click(() => removeExtension());
        }
      });
      jvn_setting_modal.modal("show");
    };

    //to save parameters and commit with those parameters
    const saveParamsAndCommit = function () {
      /**
       * Initializes a dialog modal triggered by a dropdown button on the toolbar
       *
       * Body: formParamsUI()
       *
       * Button:
       *  - Commit: store all params to window.jvn_params, and commit to Jovian
       */
      const jvn_params_modal = dialog.modal({
        show: false,
        title: "Set up Parameters to Jovian",
        body: formParamsUI,
        notebook: Jupyter.notebook,
        keyboard_manager: Jupyter.notebook.keyboard_manager,
        buttons: {
          Cancel: {},
          Commit: {
            class: "btn-primary",
            click: function () {
              storeParams();
              openModal(modalInit); // use openModal() to prevent keyboard loss when need to ask users API key
            }
          }
        },
        open: async function () {
          let project_id_helper = async () => {
            if (getParams() == null) {
              return;
            }
            let project_id = getParams().project_id;
            let j_id = "#project_id_box";
            if (project_id.length != 0 && !$(j_id).prop("disabled")) {
              $(j_id).val(project_id);
              return;
            }
            let project_title = "";
            await getProjectTitle().then(title => {
              if (title != undefined) {
                project_title = title;
              }
              if (!$(j_id).prop("disabled")) {
                $(j_id).val(project_title);
              }
            });
          };
          let git_message_helper = () => {
            if (!$("#git_msg_box").prop("disabled")) {
              $("#git_msg_box").val($("#project_msg_box").val());
            }
          };

          let params = getParams();
          if (params != null) {
            $("#project_msg_box").val(params.message);
            $("#nb_filename_box").val(params.filename);
            $("#files_box").val(params.files);
            $("#env_opt option:contains(" + params.environment + ")").prop(
              "selected",
              true
            );
            await project_id_helper();
            $("#if_new option:contains(" + params.new_project + ")").prop(
              "selected",
              true
            );
            $("#nb_opt option:contains(" + params.privacy + ")").prop(
              "selected",
              true
            );
            $("#artifacts_box").val(params.outputs);
            $("#if_git option:contains(" + params.git_commit + ")").prop(
              "selected",
              true
            );
            // $("#git_msg_box").val(params.git_message);
            git_message_helper();
          } else {
            $("#nb_filename_box").val(
              Jupyter.notebook.notebook_name.replace(".ipynb", "")
            );
            $("#env_opt option:contains('auto')").prop("selected", true);
            $("#if_new option:contains('False')").prop("selected", true);
            $("#if_git option:contains('True')").prop("selected", true);
            $("#nb_opt option:contains('auto')").prop("selected", true);
          }

          let show = (target, list) => {
            let keys = Object.keys(list);
            keys.forEach(k => {
              if ($(target + " option:selected").text() == "True") {
                $(k).prop("disabled", !list[k]);
              } else {
                $(k).prop("disabled", list[k]);
              }
              if ($(k).prop("disabled") && $(k).is("input")) {
                $(k).val("");
              }
            });
          };
          show("#if_new", { "#project_id_box": false });
          $("#if_new").change(() => {
            show("#if_new", { "#project_id_box": false });
            project_id_helper();
          });

          $(jvn_params_modal).find(".modal-content").show("fast");
        }
      });

      const modal = $(jvn_params_modal).find(".modal-content");
      modal.children().first().remove();
      modal.parent().css("width", "500px");
      modal.hide();
      jvn_params_modal.modal("show");
    };

    //just save new default parameters
    const saveParams = function () {
      /**
       * Initializes a dialog modal triggered by a dropdown button on the toolbar
       *
       * Body: formParamsUI()
       *
       * Button:
       *  - Set: store all params to window.jvn_params
       */
      const jvn_default_params_modal = dialog.modal({
        show: false,
        title: "Set Default Parameters",
        body: formParamsUI,
        notebook: Jupyter.notebook,
        keyboard_manager: Jupyter.notebook.keyboard_manager,
        buttons: {
          Cancel: {},
          Set: {
            class: "btn-primary",
            click: function () {
              storeParams();
            }
          }
        },
        open: async function () {
          let project_id_helper = async () => {
            if (getParams() == null) {
              return;
            }
            let project_id = getParams().project_id;
            let j_id = "#project_id_box";
            if (project_id.length != 0 && !$(j_id).prop("disabled")) {
              $(j_id).val(project_id);
              return;
            }
            let project_title = "";
            await getProjectTitle().then(title => {
              if (title != undefined) {
                project_title = title;
              }
              if (!$(j_id).prop("disabled")) {
                $(j_id).val(project_title);
              }
            });
          };
          let git_message_helper = () => {
            if (!$("#git_msg_box").prop("disabled")) {
              $("#git_msg_box").val($("#project_msg_box").val());
            }
          };

          let params = getParams();
          if (params != null) {
            $("#project_msg_box").val(params.message);
            $("#nb_filename_box").val(params.filename);
            $("#files_box").val(params.files);
            $("#env_opt option:contains(" + params.environment + ")").prop(
              "selected",
              true
            );
            await project_id_helper();
            $("#if_new option:contains(" + params.new_project + ")").prop(
              "selected",
              true
            );
            $("#nb_opt option:contains(" + params.privacy + ")").prop(
              "selected",
              true
            );
            $("#artifacts_box").val(params.outputs);
            $("#if_git option:contains(" + params.git_commit + ")").prop(
              "selected",
              true
            );
            // $("#git_msg_box").val(params.git_message);
            git_message_helper();
          } else {
            $("#nb_filename_box").val(
              Jupyter.notebook.notebook_name.replace(".ipynb", "")
            );
            $("#env_opt option:contains('auto')").prop("selected", true);
            $("#if_new option:contains('False')").prop("selected", true);
            $("#if_git option:contains('True')").prop("selected", true);
            $("#nb_opt option:contains('auto')").prop("selected", true);
          }

          let show = (target, list) => {
            let keys = Object.keys(list);
            keys.forEach(k => {
              if ($(target + " option:selected").text() == "True") {
                $(k).prop("disabled", !list[k]);
              } else {
                $(k).prop("disabled", list[k]);
              }
              if ($(k).prop("disabled") && $(k).is("input")) {
                $(k).val("");
              }
            });
          };
          show("#if_new", { "#project_id_box": false });
          $("#if_new").change(() => {
            show("#if_new", { "#project_id_box": false });
            project_id_helper();
          });

          $(jvn_default_params_modal).find(".modal-content").show("fast");
        }
      });

      const modal = $(jvn_default_params_modal).find(".modal-content");
      modal.children().first().remove();
      modal.parent().css("width", "500px");
      modal.hide();
      jvn_default_params_modal.modal("show");
    };

    const formDropDownUI = function () {
      /**
       * module 1:
       * Draw the dropdown menu
       **/
      const div = $("<div/>")
        .attr("id", "jvn_options")
        .addClass("btn-group-vertical")
        .attr("style", "color:black")
        .attr("style", "background-color:white");

      const option1 = $("<button/>")
        .attr("id", "jvn_module1_option1")
        .addClass("btn btn-primary")
        .text("Commit with options");

      div.append(option1);

      if (sidebarFeature) {
        const option2 = $("<button/>")
          .attr("id", "jvn_module1_option2")
          .addClass("btn btn-primary")
          .text("Open sidebar");
        div.append(option2);
      }

      if (settingsFeature) {
        const option3 = $("<button/>")
          .attr("id", "jvn_module1_option3")
          .addClass("btn btn-primary")
          .text("Settings");

        div.append(option3);
      }

      return div;
    };

    const showDropDown = function () {
      /**
       * Initializes a dialog modal triggered by a dropdown button on the toolbar
       *
       * Body: formDropDownUI()
       *
       * Button:
       *  - 1: Commit with options
       *  - 2: Open sidebar
       *  - 3: Settings
       */
      const jvn_dropdown_modal = dialog.modal({
        show: false,
        body: formDropDownUI,
        notebook: Jupyter.notebook,
        keyboard_manager: Jupyter.notebook.keyboard_manager,
        open: function () {
          $(".fade").click(() => jvn_dropdown_modal.modal("hide"));
          const option1 = $("#jvn_module1_option1");
          option1.click(() => openModal(saveParamsAndCommit));

          if (sidebarFeature) {
            const option2 = $("#jvn_module1_option2");
            option2.click(() => sidebar());
          }

          if (settingsDialog) {
            const option3 = $("#jvn_module1_option3");
            option3.click(() => openModal(settingsDialog));
          }
        }
      });
      const modal = $(jvn_dropdown_modal).find(".modal-content");
      const body = modal.find(".modal-body");
      const jvn_pos = $(jvn_btn_grp.find("button")[0]).offset();
      jvn_dropdown_modal
        .html(body.html())
        .width("140px")
        .height("100px")
        .offset({ left: jvn_pos.left, top: jvn_pos.top + 25 })
        .modal("show");
    };

    // disables the extension
    function removeExtension() {
      Jupyter.notebook.save_checkpoint();
      const remove_ext = `
import os
os.system('jovian disable-extension')`;
      Jupyter.notebook.events.one("notebook_saved.Notebook", function () {
        Jupyter.notebook.kernel.execute(remove_ext);
        confirm(
          `Disabled Jovian Extension. To re-enable it, run "jovian enable-extension" and reload.`
        ).then(location.reload());
      });
    }

    //Clears the API key
    function clearAPI() {
      new Promise(resolve => {
        const purge_api =
          "from jovian.utils.credentials import purge_creds\n" +
          "purge_creds()";

        Jupyter.notebook.kernel.execute(purge_api);
        alert("You have cleared the API key");
        resolve();
      });
    }

    //Changes the API key
    function changeAPI() {
      new Promise(resolve => {
        const purge_api =
          "from jovian.utils.credentials import purge_creds\n" +
          "purge_creds()";

        Jupyter.notebook.kernel.execute(purge_api);
        resolve();
      });
      setTimeout(() => {
        //to allow purge_api to complete
        modalInit();
      }, 400);
    }

    /* 
      Adding a button for the nbextension in the notebook's toolbar 
      */
    const prefix = "Jovian";
    //toolbar button to commit to Jovian
    const save_action = {
      icon: "fa-bookmark-o", // icon
      help: "Commit to Jovian", // tooltip
      handler: modalInit // trigger for the click
    };
    const save_action_name = Jupyter.actions.register(
      save_action,
      "commit",
      prefix
    );

    const set_params_ext_action = {
      icon: "fa-caret-down",
      help: "Show a list of parameters for user to set up",
      handler: showDropDown //saveParams
    };

    const set_params_ext_name = Jupyter.actions.register(
      set_params_ext_action,
      "set_commit_params_ext",
      prefix
    );

    const jvn_btn_grp = Jupyter.toolbar.add_buttons_group([
      save_action_name,
      set_params_ext_name
    ]);

    //adding jovian logo and Commit text next to it
    $(jvn_btn_grp.find("button")[0])
      .css(
        "background",
        // jovian logo, encoded to base64
        " url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEIAAABCCAMAAADUivDaAAAAsVBMVEUAAAAKYf8LYv8LYP8LYf8LYv8KYv8MYP8JY/8MYP8JY/8RX/8AYv8Ab/8LYv8QYv////8OZP/9/f8jZf8FYP8UYf8aY//19/8dZP8mZv8AWP8BW/8ATf/6+/8qaP8AXv8AVP8ASv8Pav8AUv9ti/8AUP/x8/9Xfv/v8v/c4v9Ccv8ARv/r7v/U2//O1v93kv9Pef9Ld//W3P9ihP87b//g5f/V3P/J0v/H0P8waf8APv8gm8uUAAAADnRSTlMA/tj33vSLy8a3fG8IB6vY0CcAAAGsSURBVFjD7ZjZdoIwEIabunRnIgmBALIIuFF3a6vv/2ClQLH1HE5j4EKt/91/853MMJNhclO3HptI+VvN9nMp4aHXUQTU6d29lBCeeg0kgkCo1y5B3HeQIqZOswRxK4yAVnVE4yQQFxPIGSM0rSLCIJbFDQTyCMOzx2vfIxQkEcCicKTrm1XEKUghQAtCFSfSVx5BUggNgiXuYlXFk92WggQCwBrrOD3G0KBMqYhglEkGEuWBTHdbBHLp9MIuTtQfmIRKf9TVpD+cDgJOQb60fIfEyRmgSoG7LmEIqrUZnEKzXxFXRE0I0A5b/kgE467LDQq//RFthgwzJs6PuZF7Lt7szJtPh/1lGGUMyPwmtB3BKweYuejjRN0wIGkWzHnuo4QhhCDxB+6qqopHPk8Hsp94nHpH8BTIfcXZ+FpYLPGuUniTiCEoPUDAt5+LIkj8nh38zebwFYhdeEc4nQMdJ1JnUZbOwtuO6Ew1gsFE10czm+cfNfMpQby0/PXYDorS2vtjCtyyiIGgxIsg9r9ne3+m98U/QVzMStOqfdWVX7irr/3yjw8ofXyoVZ+79KZpyz4GvQAAAABJRU5ErkJggg==')  no-repeat 3.5px center / 19px 17px"
      )
      .append(
        $("<span/>")
          .addClass("toolbar-btn-label")
          .attr("style", "margin-left:17px")
          .text("Commit")
      )
      .find("i")
      .removeClass("fa-bookmark-o");

    // Menubar notification when committing
    const jvn_notif = Jupyter.notification_area.widget("jvn");
    jvn_notif.inner.text("Committing to Jovian....");
    jvn_notif.element.attr("disabled", true);
    jvn_notif.element.css("background-color", "green");
    jvn_notif.inner.css("color", "white");
  }

  // function for sidebar, activates when option 2 is selected from dropdown menu
  const sidebar = function () {
    /**
     * This function displays
     * the sidebar.
     */

    // made the notebook float left
    var original = document.getElementById("notebook-container");
    original.style.width = "79%";
    original.style.cssFloat = "right";

    // add div element to the page
    var div = document.createElement("div");
    div.setAttribute("id", "sidebar");
    div.style.width = "20%";
    div.style.height = "650px";
    div.style.marginTop = "-100px";
    div.style.background = "white";
    div.style.color = "black";
    div.style.cssFloat = "left";
    div.style.position = "sticky";
    div.style.position = "fixed";

    // X button to close sidebar
    var button = document.createElement("BUTTON");
    button.innerHTML = "X";
    button.style.color = "black";
    button.style.cssFloat = "right";
    div.appendChild(button);

    // displays Jovian logo
    var Jlogo = document.createElement("IMG");
    Jlogo.setAttribute("src", "https://www.jovian.ai/jovian_logo.svg");
    Jlogo.setAttribute("width", "250px");
    div.appendChild(Jlogo);

    function display_user_and_notebook() {
      /**
       * This function displays the
       * user name and current notebook name
       * in the side bar.
       */

      let project = "";

      let label = document.createElement("div");
      label.style.color = "#585858";
      label.style.textAlign = "center";
      label.style.fontSize = "x-large";
      label.style.paddingTop = "10px";
      label.setAttribute("id", "prototypeONe");

      var content = document.createTextNode(project);
      label.appendChild(content);

      user_and_notebook();

      return label;
    }

    function display_latest_version() {
      /**
       * This function displays
       * the latest version number
       * in the sidebar
       */

      let latestVersion = "";

      let label = document.createElement("div");
      label.style.color = "#585858";
      label.style.textAlign = "center";
      label.style.fontSize = "x-large";
      label.setAttribute("id", "prototypeTwo");
      var content = document.createTextNode(latestVersion);
      label.appendChild(content);

      refresh_latest_version();

      return label;
    }

    function display_version_control() {
      /**
       * This function displays the
       * version control dropdown menu
       * in the sidebar
       */

      var html = "";

      let iframe = document.createElement("IFRAME");
      iframe.src = "data:text/html;charset=utf-8," + encodeURI(html);
      iframe.height = "140px";
      iframe.width = "250px";
      iframe.style.border = "0";
      iframe.setAttribute("id", "prototypeThree");
      document.body.appendChild(iframe);

      refresh_version_control();

      return iframe;
    }

    function display_share_dialog() {
      /**
       * This function will display the
       * share dialog in the sidebar
       */

      var html = "";

      let iframe = document.createElement("IFRAME");
      iframe.src = "data:text/html;charset=utf-8," + encodeURI(html);
      iframe.height = "140px";
      iframe.width = "250px";
      iframe.style.border = "0";
      iframe.setAttribute("id", "prototypeFour");
      document.body.appendChild(iframe);

      share_dialog();

      return iframe;
    }

    function display_collaborators() {
      /**
       * This function will display
       * collaborators in the sidebar
       */

      var html = "";

      let iframe = document.createElement("IFRAME");
      iframe.src = "data:text/html;charset=utf-8," + encodeURI(html);
      iframe.height = "190px";
      iframe.width = "250px";
      iframe.style.border = "0";
      iframe.setAttribute("id", "prototypeFive");
      document.body.appendChild(iframe);

      collaborators();

      return iframe;
    }

    // User and notebook: Section
    var User_and_Notebook = document.createElement("div");
    User_and_Notebook.style.width = "100%";
    User_and_Notebook.style.height = "40px";
    User_and_Notebook.style.borderTopColor = "blue";
    User_and_Notebook.appendChild(display_user_and_notebook());
    div.append(User_and_Notebook);

    // Latest_Version: Section
    var Latest_Version = document.createElement("div");
    Latest_Version.style.width = "100%";
    Latest_Version.style.height = "40px";
    Latest_Version.style.borderColor = "red";
    Latest_Version.appendChild(display_latest_version());
    div.append(Latest_Version);

    // Version_Control: Section
    var Version_Control = document.createElement("div");
    Version_Control.style.width = "100%";
    Version_Control.style.height = "140px";
    Version_Control.style.borderWidth = "5px";
    Version_Control.style.border = "solid";
    Version_Control.style.borderTopColor = "blue";
    Version_Control.style.borderRightColor = "white";
    Version_Control.style.borderLeftColor = "white";
    Version_Control.style.borderBottomColor = "white";
    Version_Control.appendChild(display_version_control());
    div.append(Version_Control);

    // Share Dialog: Section
    var Share_Dialog = document.createElement("div");
    Share_Dialog.style.width = "100%";
    Share_Dialog.style.height = "140px";
    Share_Dialog.style.borderWidth = "5px";
    Share_Dialog.style.border = "solid";
    Share_Dialog.style.borderTopColor = "blue";
    Share_Dialog.style.borderLeftColor = "white";
    Share_Dialog.style.borderRightColor = "white";
    Share_Dialog.style.borderBottomColor = "white";
    Share_Dialog.appendChild(display_share_dialog());
    div.append(Share_Dialog);

    // Collaborators: Section
    var collaborators_section = document.createElement("div");
    collaborators_section.width = "100%";
    collaborators_section.height = "140px";
    collaborators_section.style.borderWidth = "5px";
    collaborators_section.style.border = "solid";
    collaborators_section.style.borderTopColor = "blue";
    collaborators_section.style.borderLeftColor = "white";
    collaborators_section.style.borderRightColor = "white";
    collaborators_section.style.borderBottomColor = "blue";
    collaborators_section.appendChild(display_collaborators());
    div.append(collaborators_section);

    button.addEventListener("click", function () {
      /**
       * when sidebar is close the boolean
       * variable: sidebar_open is switch to false.
       */
      sidebar_open.value = false;

      original.style.cssFloat = "none";
      div.remove();
    });

    document.getElementById("notebook").appendChild(div);

    return original;
  };

  function openModal(func) {
    // Helper function; which use to open a new window(modal)
    // from an existing window(modal/dialog)
    return new Promise(res => {
      let len = $(".modal-backdrop").length;
      let it = setInterval(() => {
        if (len != $(".modal-backdrop").length) {
          func();
          res(clearInterval(it));
        }
      });
    });
  }

  function getArrayInPython(arrInString) {
    // Helper function; which use to format a string
    // that can be used in commit() array arguments
    // such as outputs and files
    const arr =
      "[" +
      arrInString
        .split(",")
        .map(e => "'" + e.trim() + "'")
        .join(",") +
      "]";
    if (arr == "['']") {
      return "None";
    }
    return arr;
  }

  function getValInPython(val) {
    // Helper function; which use to format a string
    // that can be used in commit() string arguments
    if (val === "") {
      return "None";
    }
    return '"' + val + '"';
  }

  function getProjectTitle() {
    return new Promise(resolve => {
      const jvnLog = data => {
        let ms = data.content.text
          .trim()
          .replace(/.*?\"/, "")
          .split('"')
          .shift();
        if (ms.toLowerCase() == "none") {
          resolve(undefined);
        }
        resolve(ms);
      };
      const code =
        "from jovian.utils.commit import _parse_project as p\n" +
        "a = p(project=None, new_project=None, filename=None)\n" +
        "print(a[0])";
      Jupyter.notebook.kernel.execute(code, {
        iopub: { output: jvnLog }
      });
    });
  }

  function storeParams() {
    // This function will be used to stored
    // the settings of parameters
    const jvn_params = {
      message: $("#project_msg_box").val(),
      filename: $("#nb_filename_box").val(),
      files: $("#files_box").val(),
      environment: $("#env_opt option:selected").text(),
      project_id: $("#project_id_box").val(),
      new_project: $("#if_new option:selected").text(),
      privacy: $("#nb_opt option:selected").text(),
      outputs: $("#artifacts_box").val(),
      git_commit: $("#if_git option:selected").text(),
      git_message: $("#git_msg_box").val()
    };

    localStorage.setItem(
      Jupyter.notebook.notebook_name,
      JSON.stringify(jvn_params)
    );
  }

  function getParams() {
    // get parameter settings from current notebook
    return JSON.parse(localStorage.getItem(Jupyter.notebook.notebook_name));
  }

  function clearParams() {
    // clear the settings of current notbbok
    localStorage.removeItem(Jupyter.notebook.notebook_name);
  }

  return {
    load_ipython_extension: loadJovianExtension
  };
});
