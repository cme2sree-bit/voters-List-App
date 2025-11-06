<h2>Search Voter</h2>
<form method="POST">
  <input type="text" name="serial" placeholder="Serial No">
  <input type="text" name="name" placeholder="Name">
  <input type="text" name="house" placeholder="House Name">
  <input type="text" name="party" placeholder="Political Party (LDF/UDF/NDA)">
  <input type="submit" value="Search">
</form>
{% if results %}
  <table border=1>
    <tr>
      {% for col in results[0].keys() %}<th>{{ col }}</th>{% endfor %}
    </tr>
    {% for v in results %}
      <tr>
        {% for c in v.values() %}<td>{{ c }}</td>{% endfor %}
      </tr>
    {% endfor %}
  </table>
{% endif %}
