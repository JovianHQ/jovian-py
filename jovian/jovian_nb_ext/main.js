define([
  "jquery",
  "base/js/namespace",
  "base/js/dialog",
  "base/js/keyboard"
], function($, Jupyter, dialog, keyboard) {
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

        const nb_filename = Jupyter.notebook.notebook_name;
        var commit = '\tcommit(nb_filename="' + nb_filename + '")\n';

        // if we have a set of params already, then use it to call commit.
        if (window.jvn_params != null) {
          const secret = window.jvn_params.secret;
          const capture_env = window.jvn_params.capture_env;
          const create_new = window.jvn_params.create_new;
          const env_type = window.jvn_params.env_type;
          const files = window.jvn_params.files;
          var notebook_id;
          const artifacts = window.jvn_params.artifacts;

          if (window.jvn_params.notebook_id === "") {
            notebook_id = "None";
          } else {
            notebook_id = '"' + window.jvn_params.notebook_id + '"';
          }

          commit =
            "commit(" +
            'nb_filename="' +
            window.jvn_params.nb_filename +
            '"' +
            ",secret=" +
            secret +
            "" +
            ",capture_env=" +
            capture_env +
            "" +
            ",create_new=" +
            create_new +
            "" +
            ",files=" +
            files +
            "" +
            ",notebook_id=" +
            notebook_id +
            "" +
            ",artifacts=" +
            artifacts +
            "" +
            ',env_type="' +
            env_type +
            '"' +
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
        Jupyter.notebook.events.one("notebook_saved.Notebook", function() {
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

    const formUI = function() {
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

      const div = $("<div/>")
        .attr("id", "input_div")
        .appendTo(form);

      const help_label = $("<label/>")
        .attr("id", "i_label")
        .text("Please enter your API key from ")
        .append(
          $("<a/>")
            .attr("href", "https://jovian.ml?utm_source=nb-ext")
            .attr("target", "_blank")
            .text("Jovian")
        );

      const input_box = $("<input/>")
        .addClass("form-control")
        .attr("id", "text_box")
        .attr("placeholder", "Paste and Save your API key");

      const error_msg = $("<label />")
        .attr("id", "e_label")
        .css("color", "red")
        .text("Invalid API key")
        .hide();

      div
        .append(help_label)
        .append(input_box)
        .append(error_msg);

      input_box.bind("keyup paste", function() {
        error_msg.hide();
        div.removeClass("has-error");
      });

      return form;
    };

    const modalInit = function() {
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
            click: function() {
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
                    "Congrats! You have saved a valid API key, now you can commit directly from the Commit toolbar button"
                  );
                }
              });
            }
          }
        },
        open: function() {
          // bind enter key for #save_button when the modal is open
          jvn_modal.find("#text_box").keydown(function(event) {
            if (event.which === keyboard.keycodes.enter) {
              jvn_modal
                .find("#save_button")
                .first()
                .click();
              return false;
            }
          });

          // Select the input when modal is open, easy to paste the key without the need for user to click first
          jvn_modal
            .find("#text_box")
            .focus()
            .select();
        }
      });
      getParams()
        .then(jvn_params => (window.jvn_params = jvn_params))
        .then(() => updateForm(jvn_modal));
    };

    const formParamsUI = function() {
      /**
       * Body of the Form
       *
       * Layout:
       *  - form : class: form-horizontal
       *    - div :
       *      - label : text: Create a secret notebook?
       *      - div   : class: form-check
       *        - input : class: form-check-input | type : raido | name : secret_opt | value : True
       *        - label : class: form-check-label | text : True  | css : margin-right:1em
       *        - input : class: form-check-input | type : raido | name : secret_opt | value : False
       *        - label : class: form-check-label | text : False
       *      - label : text: The filename of the jupyter notebook
       *      - input : id: nb_filename_box | class: form-control | value: Jupyter.notebook.notebook_name
       *      - label : text: Any additional scripts(.py files), CSVs that are required to run the notebook. These will be available in the files tab on Jovian. - array
       *      - input : id: files_box | class: form-control | value: []
       *      - label : text: To capture and and upload Python environment along with the notebook?
       *      - div   : class: form-check
       *        - input : class: form-check-input | type : raido | name : cap_opt | value : True
       *        - label : class: form-check-label | text : True  | css : margin-right:1em
       *        - input : class: form-check-input | type : raido | name : cap_opt | value : False
       *        - label : class: form-check-label | text : False
       *      - label : text: Which type of environment to be captured?
       *      - select  : id: env_opt
       *        - option : text: conda
       *        - option : text: pip   | css : margin-left : 1em
       *      - label : text: To provide the base64 ID(present in the URL) of an notebook hosted on Jovian? - String
       *      - input : id: notebook_id_box | class: form-control | value: None
       *      - label : text: To create a new notebook?
       *      - div   : class: form-check
       *        - input : class: form-check-input | type : raido | name : create_opt | value : True
       *        - label : class: form-check-label | text : True  | css : margin-right:1em
       *        - input : class: form-check-input | type : raido | name : create_opt | value : False
       *        - label : class: form-check-label | text : False
       *      - label : text: Any outputs files or artifacts generated from the modeling processing. This can include model weights/checkpoints, generated CSVs, images etc. - array
       *      - input : id: artifacts_box | class: form-control | value: []
       *
       */
      const form = $("<form/>").addClass("form-horizontal");

      const div = $("<div/>")
        .attr("id", "input_div")
        .appendTo(form);

      const secret_label = $("<label/>").text("Create a secret notebook?");
      const secret_box = $("<div/>")
        .addClass("form-check")
        .append(
          $("<input/>")
            .addClass("form-check-input")
            .attr("type", "radio")
            .attr("name", "secret_opt")
            .attr("value", "True")
        )
        .append(
          $("<label/>")
            .addClass("form-check-label")
            .text("True")
            .css("margin-right", "1em")
        )
        .append(
          $("<input/>")
            .addClass("form-check-input")
            .attr("type", "radio")
            .attr("name", "secret_opt")
            .attr("value", "False")
        )
        .append(
          $("<label/>")
            .addClass("form-check-label")
            .text("False")
        );

      const nb_filename_label = $("<label/>").text(
        "The filename of the jupyter notebook"
      );
      const nb_filename_box = $("<input/>")
        .addClass("form-control")
        .attr("id", "nb_filename_box")
        .val(Jupyter.notebook.notebook_name.replace(".ipynb", ""));

      const files_label = $("<label/>").text(
        "Any additional scripts(.py files), CSVs that are required to run the notebook. These will be available in the files tab on Jovian. - Pass the list of strings(filenames)"
      );
      const files_box = $("<input/>")
        .addClass("form-control")
        .attr("id", "files_box")
        .val("[]");

      const capture_env_label = $("<label/>").text(
        "To capture and and upload Python environment along with the notebook?"
      );
      const capture_env_box = $("<div/>")
        .addClass("form-check")
        .append(
          $("<input/>")
            .addClass("form-check-input")
            .attr("type", "radio")
            .attr("name", "cap_opt")
            .attr("value", "True")
        )
        .append(
          $("<label/>")
            .addClass("form-check-label")
            .text("True")
            .css("margin-right", "1em")
        )
        .append(
          $("<input/>")
            .addClass("form-check-input")
            .attr("type", "radio")
            .attr("name", "cap_opt")
            .attr("value", "False")
        )
        .append(
          $("<label/>")
            .addClass("form-check-label")
            .text("False")
        );

      const env_type_label = $("<label/>").text(
        "Which type of environment to be captured?"
      );
      const env_type_box = $("<select/>")
        .attr("id", "env_opt")
        .append($("<option/>").text("conda"))
        .append($("<option/>").text("pip"))
        .css("margin-left", "1em");

      const notebook_id_label = $("<label/>").text(
        "Notebook-id(optional) This is picked up by the library automatically. Incase if you want to commit to a different notebook, enter the address of that notebook like `user_name_on_jovian/notebook_name`"
      );
      const notebook_id_box = $("<input/>")
        .addClass("form-control")
        .attr("id", "notebook_id_box")
        .attr("placeholder", "None");

      const create_new_label = $("<label/>").text("To create a new notebook?");
      const create_new_box = $("<div/>")
        .addClass("form-check")
        .append(
          $("<input/>")
            .addClass("form-check-input")
            .attr("type", "radio")
            .attr("name", "create_opt")
            .attr("value", "True")
        )
        .append(
          $("<label/>")
            .addClass("form-check-label")
            .text("True")
            .css("margin-right", "1em")
        )
        .append(
          $("<input/>")
            .addClass("form-check-input")
            .attr("type", "radio")
            .attr("name", "create_opt")
            .attr("value", "False")
        )
        .append(
          $("<label/>")
            .addClass("form-check-label")
            .text("False")
        );
      const artifacts_label = $("<label/>").text(
        "Any outputs files or artifacts generated from the modeling processing. This can include model weights/checkpoints, generated CSVs, images etc. - Pass the list of strings(filenames)"
      );
      const artifacts_box = $("<input/>")
        .addClass("form-control")
        .attr("id", "artifacts_box")
        .val("[]");

      div
        .append(secret_label)
        .append(secret_box)
        .append("<br>")
        .append(nb_filename_label)
        .append(nb_filename_box)
        .append("<br>")
        .append(files_label)
        .append(files_box)
        .append("<br>")
        .append(capture_env_label)
        .append(capture_env_box)
        .append("<br>")
        .append(env_type_label)
        .append(env_type_box)
        .append("<br>")
        .append(notebook_id_label)
        .append(notebook_id_box)
        .append("<br>")
        .append(create_new_label)
        .append(create_new_box)
        .append("<br>")
        .append(artifacts_label)
        .append(artifacts_box);

      return form;
    };

    const saveParams = function() {
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
          Commit: {
            id: "save_params_button",
            class: "btn-primary",
            click: function() {
              storeParamsInPython();
              modalInit();
            }
          }
        },
        open: function() {
          getParams().then(jvn_params => {
            if (jvn_params == null) {
              $("#nb_filename_box").val(
                Jupyter.notebook.notebook_name.replace(".ipynb", "")
              );
              $($("input[name=secret_opt")[1]).prop("checked", true);
              $($("input[name=cap_opt")[0]).prop("checked", true);
              $($("input[name=create_opt")[1]).prop("checked", true);
              $("#env_opt option:contains('conda')").prop("selected", true);
            } else {
              $("#nb_filename_box").val(
                jvn_params.nb_filename.replace(".ipynb", "")
              );
              jvn_params.secret == "False"
                ? $($("input[name=secret_opt")[1]).prop("checked", true)
                : $($("input[name=secret_opt")[0]).prop("checked", true);
              jvn_params.capture_env == "False"
                ? $($("input[name=cap_opt")[1]).prop("checked", true)
                : $($("input[name=cap_opt")[0]).prop("checked", true);
              jvn_params.create_new == "False"
                ? $($("input[name=create_opt")[1]).prop("checked", true)
                : $($("input[name=create_opt")[0]).prop("checked", true);
              jvn_params.env_type == "conda"
                ? $("#env_opt option:contains('conda')").prop("selected", true)
                : $("#env_opt option:contains('pip')").prop("selected", true);
            }
          });
        }
      });
      jvn_params_modal.modal("show");
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
      icon: "fa-angle-double-down",
      help: "Show a list of parameters for user to set up",
      handler: saveParams
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
        " url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB4AAAAjCAIAAAAMti2GAAABTGlDQ1BpY2MAACjPY2BgUkksKMhhYWBgyM0rKQpyd1KIiIxSYH/IwA6EvAxiDAqJycUFjgEBPkAlDDAaFXy7xsAIoi/rgsw6JTW1SbVewNdipvDVi69EmxjwA66U1OJkIP0HiFOTC4pKGBgYU4Bs5fKSAhC7A8gWKQI6CsieA2KnQ9gbQOwkCPsIWE1IkDOQfQPIVkjOSASawfgDyNZJQhJPR2JD7QUBbpfM4oKcxEqFAGMGqoOS1IoSEO2cX1BZlJmeUaLgCAylVAXPvGQ9HQUjA0NzBgZQmENUfw4EhyWj2BmEWPN9Bgbb/f///9+NEPPaz8CwEaiTaydCTMOCgUGQm4HhxM6CxKJEsBAzEDOlpTEwfFrOwMAbycAgfAGoJ7o4zdgILM/I48TAwHrv///PagwM7JMZGP5O+P//96L///8uBmq+w8BwIA8AFSFl7ghfNBMAAAAgY0hSTQAAeiYAAICEAAD6AAAAgOgAAHUwAADqYAAAOpgAABdwnLpRPAAAAAZiS0dEAP8A/wD/oL2nkwAAAAd0SU1FB+MIBgkzIxDC+FwAAANlSURBVEjHtZZNTxtHGMf/M+O3uA5OttgG27UxSmrSppEhRJzKxTckc6nEuQeOfAOuPcIFiS/ByQcUwQfgVGMhgtI3NTah1KwJccB2bNaeeXpYt8QvyGvTzGm1+9+fnvnNPrPDiAifZ9j6JhoShyeyek0AOMOToPjSw/4fdP6dWntZ//CRAGge9tMP9yyied/EwbEsVQmAVHgcEKGHPV6RUg6Mrhm0n28qAgAbx4uYcLTPs1wur62tLS0tbW5u1mq1AYTk36k/i4pzEGF0hD2LiI5AOp1eXV01DGN3dzcSiaRSKatVZ/OyXCMGKMKTcTHu7czrum4YBoB6vV4qlawKqVxT9lia36ZdYHZS2DqLRiqVSiaTPp9vcXExmUxaFfKmqPLnijEQweflT8OiOxOPx7e2tnRdDwaDXq/XKno/LyvXxBkk4dsQD4z0nqKmaZqmdd+/FX1Vo4PjpnntsOFFzCZ6kYnIMAwi4pzb7XbGbj75W13/oau3F4oxKMKYl38TEj1jxWJxeXl5YWFhZWWlUqlYqno/1/xogDMowndh4bvfuwPr9fre3l4ulzs/P280Gp8+6l11qUoHb1sN5rJjdlIwS73dNnqjfzuTp++VWXLwAZ8aFwNib0ETIZOTNXNyhGcRoVnbj/qjLyp0eCJNAy4HZmNiGHBP9C8FWfjQsvGVxr8eG8ZGD7QiZN7I63+XOhEVD9zDFd2FLl6pV39JxkCA28GeT/T/V1hFvz5V+pXiDESIjvJHgf7/CktoqfBzrtlotTdmouK+a0gbneizS/X6VHIGAjwuNjMx5AL2QL86kedlYgykMOnjMd/wNtrQDYlMTjYlADCGmQnxhXN4G23ov0vq14I0F3DkHpuJ3slGG/rwRF5UyNxFHwV4dPRONm7QRhOZnJQKADjH85jNZb+TjRv0yXv1+1nLxkM3S0Ss2pBSmucbIQRr33lb6Gy+eVEhApoKj8dEWLNqI5/Pm2cEv9/vdDo/fWQDQEBY4z9+7zC3pKdh4by9vS8vL9PpdCKRCAQChUJhfX29XC4DmJubc7vdbVEacGxvb3s8Hr/fH4/H/X6/KSEejx8dHXUkB0ZvbGx4PJ7/KhNCTE9P7+zsdCfZoEf3arWayWSy2ayu606nc2pqan5+PhQKdScHRlsf/wCBmeWmRK6m9QAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAxOS0wOC0wNlQwOTo1MTozNS0wNDowMBKu+PQAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMTktMDgtMDZUMDk6NTE6MzUtMDQ6MDBj80BIAAAAAElFTkSuQmCC') no-repeat 5px / 15px 17px"
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
  }

  function storeParamsInPython() {
    // This function will be used to stored
    // the set of parameters into Python
    // and then we can call getParams()
    // to get these data
    const jvn_params = {
      secret: $("input[name=secret_opt]")
        .filter(":checked")
        .val(),
      nb_filename: $("#nb_filename_box").val() + ".ipynb",
      files: $("#files_box").val(),
      capture_env: $("input[name=cap_opt]")
        .filter(":checked")
        .val(),
      env_type: $("#env_opt option:selected").text(),
      notebook_id: $("#notebook_id_box").val(),
      create_new: $("input[name=create_opt]")
        .filter(":checked")
        .val(),
      artifacts: $("#artifacts_box").val()
    };

    const python_id = getStoredId();
    const var_in_python = python_id + " = " + JSON.stringify(jvn_params);
    const store_to_python = "%store " + python_id;
    Jupyter.notebook.kernel.execute(var_in_python + "\n" + store_to_python);
  }

  function getParams() {
    // This function we use to check if we
    // have set parameters of jovian.commit()
    // already.
    // If so, we return these parameter,
    // otherwise, just return null.
    const python_id = getStoredId();
    const check_params =
      python_id +
      ' = "F8612598845FB14364EC59A2528862E18664728B4FC319C6F4BB817CB16F6D23AB752E247FF806C6D5730567025A886E765E19F764802E87F871CAB4C72B540E"\n' +
      "%store -r " +
      python_id +
      "\n" +
      "print (" +
      python_id +
      ")";
    return new Promise((resolve, reject) => {
      Jupyter.notebook.kernel.execute(check_params, {
        iopub: {
          output: data => resolve(data.content.text.trim())
        }
      });
    }).then(result => {
      if (
        !result.includes(
          "F8612598845FB14364EC59A2528862E18664728B4FC319C6F4BB817CB16F6D23AB752E247FF806C6D5730567025A886E765E19F764802E87F871CAB4C72B540E"
        )
      ) {
        const raw_params = result
          .replace(/"/g, "{_dc_}")
          .replace(/\\'/g, "{_sc_}");
        var jvn_params = JSON.parse(raw_params.replace(/'/g, '"'));
        const nb_filename = jvn_params.nb_filename
          .replace(/{_dc_}/g, '"')
          .replace(/{_sc_}/g, "'");
        const files = jvn_params.files
          .replace(/{_dc_}/g, '"')
          .replace(/{_sc_}/g, "'");
        const artifacts = jvn_params.artifacts
          .replace(/{_dc_}/g, '"')
          .replace(/{_sc_}/g, "'");

        const notebook_id = jvn_params.notebook_id
          .replace(/{_dc_}/g, '"')
          .replace(/{_sc_}/g, "'");

        jvn_params.nb_filename = nb_filename;
        jvn_params.files = files;
        jvn_params.artifacts = artifacts;
        jvn_params.notebook_id = notebook_id;

        return jvn_params;
      }
      return null;
    });
  }

  function getStoredId() {
    // This function will be used to
    // normalize the name of notebook
    const notebookId = Jupyter.notebook.notebook_name.replace(".ipynb", "");
    const nomalizedId = notebookId.replace(
      /&|-|\[|\]|\.|,|=|\(|\)|\{|\}|\||`|~|\"|@|#|\$|\%|\^|\*|\+|\!|\<|\>|\;|\'|\?|\ /g,
      "_"
    );
    const pythonId = "stored_params_for_" + nomalizedId + "_E4CBF73";
    return pythonId;
  }

  return {
    load_ipython_extension: loadJovianExtension
  };
});
