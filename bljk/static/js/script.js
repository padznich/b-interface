$(function() {

    $("a#detail_check").on("click", function() {
        var _detail_id = $(this).find("input").attr("value");
        var _state = !$(this).find("input").prop("checked");

        $.ajax({
            type: "POST",
            contentType: 'application/json; charset=UTF-8',
            url: "/ajax/",
            data: JSON.stringify({detail_id: _detail_id, state: _state}),
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            },
            dataType: "json"
        });
    });
});