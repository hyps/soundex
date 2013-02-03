%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)
<p>Transcriptions:</p>
<a href="/view/{{left}}">prev</a>&nbsp;Total count: {{count}}&nbsp;<a href="/view/{{right}}">next</a>
<table border="0">
%for row in rows:
  <tr>
  %for col in row:
    <td>{{!col}}</td>
  %end
  </tr>
%end
</table>
<p>Add new:</p>
<form action="/submit" method="post" enctype="multipart/form-data">
<input type="text" size="10" maxlength="10" name="attribute1"/>
<input type="text" size="10" maxlength="10" name="attribute2"/>
<input type="file" name="sound"/>
<input type="submit" name="submit" value="submit"/>
</form>
<p>Drop:</p>
<form action="/drop" method="get">
<input type="submit" name="drop" value="drop"/>
</form>