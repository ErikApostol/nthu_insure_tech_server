async function insert_data() {
    const response = await fetch("/get_result");
    const data = await response.json();

    var tbody = document.getElementById("result_tbody");

    console.log(data);
    
    for(var i=0; i<data["count"]; i++) {
        var tr = document.createElement("tr");
        var tmp_data = data["content"][i];

        var td_video_id = document.createElement("td");
        var td_username = document.createElement("td");
        var td_accident_time = document.createElement("td");
        var td_file_name = document.createElement("td");
        var td_analysis_status = document.createElement("td");
        var td_analysis_info = document.createElement("td");
        
        var btn_a = document.createElement('a');
        btn_a.href = "/get_result_content?video_id=" + tmp_data["video_id"];
        
        var btn = document.createElement('input');
        btn.type = "button";
        btn.className = "btn btn-primary";
        btn.value = "詳細結果";

        btn_a.appendChild(btn);
        td_analysis_info.appendChild(btn_a);

        td_video_id.innerHTML = i;
        td_username.innerHTML = tmp_data["user_name"];
        td_accident_time.innerHTML = tmp_data["insert_time"];
        td_file_name.innerHTML = tmp_data["video_filename"];
        td_analysis_status.innerHTML = tmp_data["analysis_state"];

        // td_analysis_info.setAttribute('html', "<input type=\"button\" class=\"btn\" value=\'" + entry.email + "\" onclick=\"" + chooseUser(entry) + "\"/>");
        // td_analysis_info.appendChild(bt_analysis_info);

        tr.appendChild(td_video_id);
        tr.appendChild(td_file_name);
        tr.appendChild(td_username);
        tr.appendChild(td_accident_time);
        tr.appendChild(td_analysis_status);
        tr.appendChild(td_analysis_info);

        tbody.appendChild(tr); 
    }
}

insert_data();
