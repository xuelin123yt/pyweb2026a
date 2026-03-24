<!DOCTYPE html>
<html lang="zh-TW">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>王奕翔簡介</title>
	<style type="text/css">
		* { font-family:"標楷體"; margin-left:auto; margin-right:auto;}
		h1 {color:blue; font-size:60px;}
		h2 {color:#33ff33; font-size:40px;}
	</style>

	<script>
		function change1() {
  			document.getElementById("pic").src = "mountain.jpg";
  			document.getElementById("h2text").innerText = "靜宜資管";
		}

		function change2() {
  			document.getElementById("pic").src = "cliff.jpg";
  			document.getElementById("h2text").innerText = "YI-SIANG WANG";
		}
	</script>
</head>
<body>
<?php echo date("Y-m-d") ?>
	<table width="70%">
	    <tr>
	        <td>
	            <img src="cliff.jpg" width="110%" id="pic" onmouseover="change1()" onmouseout="change2()">
	        </td>

	        <td>
	            <h1>王奕翔</h1>
	            <h2 id="h2text">>YI-SIANG WANG</h2>
	        </td>
	    </tr>
	</table>

	<br>

	<table width="70%" border="1">
		<tr>
			<td>
				FB：<a href="https://www.facebook.com/share/1CFt8g6Apc" target="_blank">
				https://www.facebook.com/share/1CFt8g6Apc</a><br>

				IG：<a href="https://www.instagram.com/baiyue_001?igsh=MTR5NWZidXF3Y2kxZA==" target="_blank">
				https://www.instagram.com/baiyue_001?igsh=MTR5NWZidXF3Y2kxZA==</a><br>

				E-Mail: <a href="mailto:s1131212@o365st.pu.edu.tw">
				s1131212@o365st.pu.edu.tw</a><br>
			</td>

			<td>
				大象席地而坐電影配樂<br>
				<audio controls>
					<source src="elephant.mp3" type="audio/mp3">
				</audio><br>
			</td>

			<td>
				不要去臺灣<br>
				<iframe src="https://www.youtube.com/embed/pW88QFpHXa8"
				        width="300" height="200"
				        allowfullscreen>
				</iframe>
			</td>
		</tr>
	</table>

</body>
</html>