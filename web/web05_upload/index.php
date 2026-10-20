<?php
if($_SERVER['REQUEST_METHOD']==='POST') {
 if(!isset($_FILES['avatar'])){http_response_code(400);exit('missing avatar');}
 if($_FILES['avatar']['type']!=='image/png' && $_FILES['avatar']['type']!=='image/jpeg'){http_response_code(400);exit('Content-Type denied');}
 $name=basename($_FILES['avatar']['name']);
 if(!move_uploaded_file($_FILES['avatar']['tmp_name'],__DIR__.'/uploads/'.$name)){http_response_code(500);exit('upload failed');}
 echo 'Uploaded: <a href="/uploads/'.htmlspecialchars($name).'">'.$name.'</a>';
 exit;
}
?><h1>SPK Photo Studio</h1><form method="POST" enctype="multipart/form-data"><input type="file" name="avatar"><button>Upload avatar</button></form>
