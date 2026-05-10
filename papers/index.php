<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Listado de PDFs y carpetas</title>
  <style>
    body { font-family: Arial, sans-serif; background: #f9f9f9; padding: 20px; }
    ul { list-style: none; padding: 0; }
    li { margin: 5px 0; }
    a { text-decoration: none; color: #0077cc; }
    a:hover { text-decoration: underline; }
  </style>
</head>
<body>
  <h1>Documentos PDF y carpetas</h1>
  <ul>
    <?php
    $items = scandir(".");
    foreach ($items as $item) {
      if ($item === "." || $item === ".." || $item === "index.php" || $item === "pdf_index.php") continue;

      if (is_dir($item)) {
        echo "<li>📁 <a href=\"$item/\">$item/</a></li>\n";
      } elseif (preg_match('/\.pdf$/i', $item)) {
        echo "<li>📄 <a href=\"$item\">$item</a></li>\n";
      }
    }
    ?>
  </ul>
</body>
</html>
