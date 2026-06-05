async function validateJSON(){

    let jsonData =
        JSON.parse(
            document.getElementById("jsonInput").value
        );

    const response = await fetch(
        "/validate",
        {
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify(jsonData)
        }
    );

    const result = await response.json();

    document.getElementById("result")
        .innerText =
        JSON.stringify(result,null,2);
}