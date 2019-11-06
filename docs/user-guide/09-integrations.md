## Slack Notifications

Get notifications from your training experiment and stay updated with all the milestones of your code. No more watching the progress bar of your fit function to keep track of your model training.
Use the same integration to get notification about other activities on Jovian.

### Connect to a Slack Workspace

Visit [Jovian](https://jovian.ml?utm_source=docs) and click on the `Connect Slack`. You'll be redirected to Slack Webpage. 

<img src="https://i.imgur.com/9NTbh7v.png" class="screenshot">

Choose a workspace from the top right corner and a channel to integrate our Slack app. By clicking on `Allow` integration will be completed and will get a acknowledgement on the selected channel, this is where you'll be getting all your notifications.

```eval_rst
.. note::
        We suggest you to create your own `Slack Workspace`_ so that you won't spam with notifications on a public workspace.
.. _Slack Workspace: https://slack.com/create#email
```

<img src="https://imgur.com/SkK7FGC.png" class="screenshot">

### Integration Preferences 

You can customize on what notifications you get to your Slack. To update the preferences visit [Jovian Integrations](https://jovian.ml/settings/integrations?utm_source=docs) or you go to your `Profile Dropdown` on the top right corner and click on `Integrations`.

<img src="https://i.imgur.com/C2oZohS.png" class="screenshot">

### Send Notifications from your script

This will be helpful to get updates on while training a model. You can send any `python dict` or `string`, it can be when some milestones are reached or about the metrics.

<img src="https://imgur.com/IZYrKD0.png" class="screenshot">

We have this integrated to our callbacks to get automated notifications about the metrics, check out [Callbacks Section](../callbacks/keras).

For API documentation check out [Slack Notify](../jvn/notif)