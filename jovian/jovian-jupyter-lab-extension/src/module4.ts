import NBKernel from './NBKernel';


/************************ Module_4: Share Dialog ***********************************/


async function getUrl():Promise<string> {
  /**
   * This is a helper function to generate a project URL for later use.
   * the URL will be read by the shareWindow function.
   */
  const rc =
    /**
     * The following is python code. the variable
     * i will read the notebook name. the variable 
     * x will open the the rc file. x = lib[i] will 
     * match the current notebook name with the 
     * appropriate id in the lib rc. the i2 = i[:-6] 
     * will get rid of of .pynd , then the url will be 
     * generated with the following line of code.
     * URL = 'https://jovian.ml/'+i2+'/'+x2'
     */
    "from jovian.utils.jupyter import get_notebook_name\n"+
    "from jovian.utils.jupyter import get_notebook_history\n"+
    "from jovian.utils.jupyter import set_notebook_name\n"+
    "from jovian.utils.jupyter import get_notebook_path\n"+
    "from jovian.utils.jupyter import get_notebook_path_py\n"+
    "i = get_notebook_name()\n"+
    "import json\n"+
    "with open('.jovianrc') as f:\n"+
    "\tjovianrc = json.load(f)\n"+
    "lib = jovianrc['notebooks']\n"+
    "x = lib[i]\n"+
    "x2 = x['slug']\n"+
    "i2 = i[:-6]\n"+
    "URL = 'https://jovian.ml/'+i2+'/'+x2\n"+
    "print(URL)";
  let result;

  await NBKernel.execute(rc).then(
    rs => {
      result = rs;
    }
  );

  return result;
}

function shareWindow(url:string): HTMLIFrameElement{
  /**
   * This function generates a window that displays
   * the social media buttons. The buttons are the following: 
   * facebook, twitter, linkedin, and  copy link.
   * These buttons will share the current notebook that 
   * was commited to Jovian.
   */
  let facebook:string = shareToFacebook(url).outerHTML;
  let twitter:string = shareToTwitter(url).outerHTML;
  let linkedin:string = shareToLinkedIn(url).outerHTML;;
  let copylink:string = "<div><input type='text' value='" + url + "' id='myInput'><button onclick = 'myFunction()'>Copy Link</button><script>function myFunction(){var copyText = document.getElementById('myInput'); copyText.select(); copyText.setSelectionRange(0, 99999); document.execCommand('copy'); alert('Copied the link: ' + copyText.value);}</script></div>";

  var html = '<html><body><h>'+facebook+'</h><br><br><h>'+twitter+'</h><br><h>'+linkedin+'</h><br><h>'+copylink+'</h></body></html>';
  let iframe:HTMLIFrameElement = document.createElement("iframe");
      iframe.src = 'data:text/html;charset=utf-8,' + encodeURI(html);
      iframe.height = '170px';
      document.body.appendChild(iframe);
      return iframe;
}

function shareToFacebook(url: string, button: HTMLElement = null):HTMLElement {
  let html = "<script async defer crossorigin='anonymous' src='https://connect.facebook.net/en_US/sdk.js#xfbml=1&version=v5.0'></script><div class='fb-share-button' data-layout='button_count' data-size='large'><a target='_blank' href='https://www.facebook.com/sharer/sharer.php?u="
    + url 
    + "' class='fb-xfbml-parse-ignore'>";
  if (button == null) {
    html += "</a>";
  } else {
    html += button.outerHTML + "</a>";
  }
  let div:HTMLElement = document.createElement("div");
  div.innerHTML = html;
  return div;
}

function shareToTwitter(url: string, button: HTMLElement = null, defaultText:string = 'Share%20from%20Jovian'):HTMLElement {
  let html = '<a target="_blank" href="https://twitter.com/intent/tweet?original_referer=https%3A%2F%2Fpublish.twitter.com%2F%3FbuttonType%3DTweetButton%26widget%3DButton&amp;ref_src=twsrc%5Etfw&amp;text='
    + defaultText
    + '%0a&amp;url='
    + url
    + '">';
  if (button == null) {
    html += "</a>";
  } else {
    html += button.outerHTML + "</a>";
  }
  let div:HTMLElement = document.createElement("div");
  div.innerHTML = html;
  return div;
}

function shareToLinkedIn(url: string, button: HTMLElement = null):HTMLElement {
  let html = '<a target="_blank" href="https://www.linkedin.com/shareArticle?mini=true&url='
    + url
    + '">';
;
  if (button == null) {
    html += "</a>";
  } else {
    html += button.outerHTML + "</a>";
  }
  let div:HTMLElement = document.createElement("div");
  div.innerHTML = html;
  return div;
}

export { getUrl, shareWindow, shareToFacebook, shareToTwitter, shareToLinkedIn };