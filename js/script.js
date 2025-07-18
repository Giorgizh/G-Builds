var div = document.getElementById('filter');
var display = 0;

function hideShow()
{
    if(display == 1)
    {
        div.style.display = 'flex';
        display = 0;
    }
    else
    {
        div.style.display = 'none';
        display = 1;
    }
}