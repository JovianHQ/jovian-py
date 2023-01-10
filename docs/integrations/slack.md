# Slack Notifications

```eval_rst
.. meta::
   :description: Jovian integration with Slack.
```

Get notifications from your training experiment and stay updated with all the milestones of your code. No more watching the progress bar of your fit function to keep track of your model training.
Use the same integration to get notification about other activities on Jovian.

### Connect to a Slack Workspace

Visit <a href="https://jovian.com?utm_source=docs" target=_blank> Jovian </a> and click on the `Connect Slack`. You'll be redirected to Slack Webpage.

<img src="https://i.imgur.com/9NTbh7v.png" class="screenshot" alt="docs images" >

Choose a workspace from the top right corner and a channel to integrate our Slack app. By clicking on `Allow`, integration will be completed and will get a acknowledgement on the selected channel, this is where you'll be getting all your notifications.

```eval_rst
.. important::
        We suggest you to create your own `Slack Workspace`_ so that you won't spam with notifications on a public workspace. Or you can choose your DM instead if you don't want to create a new workspace.
.. _Slack Workspace: https://slack.com/create#email
```

<img src="https://imgur.com/SkK7FGC.png" class="screenshot" alt="docs images" >

### Send Notifications from your script

This will be helpful to get updates on while training a model. You can send any `python dict` or `string`, it can be when some milestones are reached or information about the metrics(accuracy, loss ...).

<img src="https://imgur.com/IZYrKD0.png" class="screenshot" alt="docs images" >

We have this integrated to our callbacks to get automated notifications about the metrics, check out [Callbacks Section](../callbacks/keras).

For API documentation check out [Jovian Slack Notify](../api-reference/notif)

### Integration Preferences

You can customize on what notifications you get to your Slack. To update the preferences visit <a href="https://jovian.com/settings/integrations?utm_source=docs" target=_blank> Jovian Settings </a> or you go to your `Profile Dropdown` on the top right corner and click on `Settings`.

<img src="https://i.imgur.com/C2oZohS.png" class="screenshot" alt="docs images" >
