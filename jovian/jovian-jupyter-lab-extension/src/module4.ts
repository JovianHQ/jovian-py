import NBKernel from './NBKernel';


/************************ Module_4: Share Dialog ***********************************/


async function getUrl():Promise<string> {
/*
This is a helper function to generate a project URL for later use.
the URL will be read by the shareWindow function.
*/
const rc =
/*
        The following is python code. the variable
        i will read the notebook name. the variable 
        x will open the the rc file. x = lib[i] will 
        match the current notebook name with the 
        appropriate id in the lib rc. the i2 = i[:-6] 
        will get rid of of .pynd , then the url will be 
        generated with the following line of code.
        URL = 'https://jovian.ml/'+i2+'/'+x2'
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

function shareWindow(text:string): HTMLIFrameElement{
  /*
  This function generates a window that displays
  the social media buttons. The buttons are the following: 
  facebook, twitter, linkedin, and  copy link.
  These buttons will share the current notebook that 
  was commited to Jovian.
  */

  let facebook:string = "<div><script async defer crossorigin='anonymous' src='https://connect.facebook.net/en_US/sdk.js#xfbml=1&version=v5.0'></script><script type='text/javascript'>var V = tt;</script><div class='fb-share-button' data-href='"+text+"' data-layout='button_count' data-size='large'><a target='_blank' href='https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fjovian.ml%2F&amp;src=sdkpreparse' class='fb-xfbml-parse-ignore'></a></div>";
  let twitter:string = '<div><a class="twitter-share-button" href="https://twitter.com/intent/tweet" data-size="large" data-text="custom text" data-url='+text+' data-hashtags="" data-via="" data-related="twitterapi,twitter">Tweet</a><script>window.twttr = (function(d, s, id) { var js, fjs = d.getElementsByTagName(s)[0], t = window.twttr || {}; if (d.getElementById(id)) return t; js = d.createElement(s); js.id = id; js.src = "https://platform.twitter.com/widgets.js"; fjs.parentNode.insertBefore(js, fjs); t._e = []; t.ready = function(f) { t._e.push(f);}; return t;} (document, "script", "twitter-wjs"));</script></div>';
  let linkedin:string = "<div><script src='https://platform.linkedin.com/in.js' type='text/javascript'>lang: en_US</script><script type='IN/Share' data-url='"+text+"'></script></div>";
  let copylink:string = "<div><input type='text' value='"+text+"' id='myInput'><button onclick = 'myFunction()'>Copy Link</button><script>function myFunction(){var copyText = document.getElementById('myInput'); copyText.select(); copyText.setSelectionRange(0, 99999); document.execCommand('copy'); alert('Copied the link: ' + copyText.value);}</script></div>";

  var html = '<html><body><h>'+facebook+'</h><br><br><h>'+twitter+'</h><br><h>'+linkedin+'</h><br><h>'+copylink+'</h></body></html>';
  let iframe:HTMLIFrameElement = document.createElement("iframe");
      iframe.src = 'data:text/html;charset=utf-8,' + encodeURI(html);
      iframe.height = '170px';
      document.body.appendChild(iframe);
      return iframe;
    }


export { getUrl, shareWindow };