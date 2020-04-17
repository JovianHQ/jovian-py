define([
  "jquery",
  "base/js/namespace",
  "base/js/dialog",
  "base/js/keyboard"
], function ($, Jupyter, dialog, keyboard) {
  function loadJovianExtension() {
    /**
     *  Jupyter extension to commit the notebook to Jovian.
     *
     *  Commits the notebook if there is a valid API key available
     *  else prompts the user with a modal to get the API key.
     */

    const jvnCommit = () =>
      /**
       * Commits the notebook to Jovian(https://jovian.ml).
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
        let commit = "\tcommit(filename=" + getValInPython(filename) + ")\n";
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
            ")\n";
        }

        const jvn_commit =
          "from jovian import commit\n" +
          "import io\n" +
          "from contextlib import redirect_stdout\n" +
          "f = io.StringIO()\n" +
          "with redirect_stdout(f):\n" +
          "\t" +
          commit +
          "out = f.getvalue().splitlines()[-1]\n" +
          "if(out.split()[1] == 'Committed'):\n" +
          "\tprint(out.split()[-1])\n" +
          "else:\n" +
          "\tprint(out)";

        /* Saves the notebook creates a checkpoint and then commits*/
        Jupyter.notebook.save_checkpoint();
        Jupyter.notebook.events.one("notebook_saved.Notebook", function () {
          Jupyter.notebook.kernel.execute(jvn_commit, {
            iopub: { output: jvnLog }
          });
        });
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
              function copyToClipboard() {
                jvn_modal
                  .find("#i_label")
                  .append($("<textarea>").val(log_data)); // temp element
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
              if (log_data.startsWith("https://")) {
                const nb_link = $("<a/>")
                  .attr("href", log_data)
                  .attr("target", "_blank")
                  .text(log_data);

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
                  .text("Committed Successfully! ")
                  .append($("<br/>"))
                  .append(nb_link)
                  .append(copy_btn);
              } else {
                jvn_modal.find("#i_label").text("Commit failed! " + log_data);
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
       *      - label : id: i_label | text: Please enter your API key from [Jovian](https://jovian.ml)
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
      //     .attr("href", "https://jovian.ml?utm_source=nb-ext")
      //     .attr("target", "_blank")
      //     .text("Jovian")
      // );

      const input_box = $("<input/>")
        .addClass("form-control")
        .attr("id", "text_box")
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

    const saveParams = function () {
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

      // const option2 = $("<button/>")
      //   .attr("id", "jvn_module1_option2")
      //   .addClass("btn btn-primary")
      //   .text("Open sidebar");

      // const option3 = $("<button/>")
      //   .attr("id", "jvn_module1_option3")
      //   .addClass("btn btn-primary")
      //   .text("Settings");

      div.append(option1);

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
          const option2 = $("#jvn_module1_option2");
          const option3 = $("#jvn_module1_option3");
          option1.click(() => openModal(saveParams));
          option2.click(() => alert("feature coming soon"));
          option3.click(() => openModal(clearParams));
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

    //toolbar button to remove the jovian extension
    const set_params_ext_action = {
      icon: "fa-caret-down",
      help: "Show a list of parameters for user to set up",
      handler: showDropDown //saveParams
    };
    const set_params_ext_name = Jupyter.actions.register(
      set_params_ext_action,
      "set_params_ext",
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
