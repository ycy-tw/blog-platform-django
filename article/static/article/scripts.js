$(document).ready(function () {

    // $("#menu-btn").on("click", function () {
    //     $("#sidebar").toggleClass("active");
    //     $("#content").toggleClass("active");
    // });

    $("label[for='id_body']").remove(); // label of body must have text to make ckeditor css effect.

    // because origin textarea for body field will be hide after using ckeditor,
    // if the required attribute still exist, the form can not be submit.
    $("textarea[id=id_body]").removeAttr('required');

    $("textarea[name=description]").on("keyup keydown", UpdateCount);

    // for search autocomplete
    $(function () {
        $("#search").autocomplete({
            source: "/",
        });
    });

    // remove content div when no h1, h2, h3 in articles.
    $(function () {
        if ($('#toc-ul').is(':empty')) {
            $('#toc-ul').parent().remove();
        }
    });
});

function UpdateCount() {
    // show count of description text in real-time
    $('#characters').text($(this).val().length + ' / 100');
}


// follow function
$(document).on("click", "#follow-btn", function (e) {

    e.preventDefault();
    // Following = $.trim($("#uid").text()).substring(1);
    Following = $("#uid").val();
    Follow(Following);

});


// follow function for follow-list
$(document).on("click", ".follow-btn", function (e) {

    e.preventDefault();
    Following = $(this).closest('div').find('.uid').val();
    FollowInUserList(Following, $(this));

});


function Follow(User) {
    $.ajax({
        url: "/follow",
        type: "POST",
        data: {
            "Following": Following,
        },
        success: function (response) {

            Status = response.status
            if (Status == "success") {

                FollowOrUnfollow = response.action;

                if (FollowOrUnfollow === "Follow") {

                    $("#follow-btn").text("Following");
                    FollowerCount = Number($.trim($("#follower-count").text()));
                    $("#follower-count").text(FollowerCount + 1);
                    $("#follow-btn").toggleClass("theme-btn-fill");
                    $("#follow-btn").toggleClass("theme-btn");


                } else if (FollowOrUnfollow === "Unfollow") {

                    $("#follow-btn").text("Follow");
                    FollowerCount = Number($.trim($("#follower-count").text()));
                    $("#follower-count").text(FollowerCount - 1);

                    $("#follow-btn").toggleClass("theme-btn");
                    $("#follow-btn").toggleClass("theme-btn-fill");

                }

            } else {

                Action = response.action;
                if (Action == "RedirectLogIn") {
                    window.location.href = "/account/login";
                }

            }
        }
    })
}


function FollowInUserList(User, Button) {
    $.ajax({
        url: "/follow",
        type: "POST",
        data: {
            "Following": Following,
        },
        success: function (response) {

            Status = response.status
            if (Status == "success") {

                FollowOrUnfollow = response.action;

                if (FollowOrUnfollow === "Follow") {

                    $(Button).text("Following");
                    $(Button).toggleClass('theme-btn theme-btn-fill');


                } else if (FollowOrUnfollow === "Unfollow") {

                    $(Button).text("Follow");
                    $(Button).toggleClass('theme-btn-fill theme-btn');

                }
            } else {

                Action = response.action;
                if (Action == "RedirectLogIn") {
                    window.location.href = "/account/login";
                }

            }
        }
    })
}

//-------------------------//
//  User Edit Form         //
//-------------------------//

$(document).on("click", "#profile-edit-btn", function (e) {
    e.preventDefault();
    // Username = $.trim($(this).parent().parent().find("#uid").text()).substring(1);
    $(".profile-info").css("display", "none");
    $("#user-edit-form").css("display", "block");
});

// $(document).on("click", "#save-edit", function (e) {

//     e.preventDefault();

//     var data = new FormData();

//     Username = $("#uid").val();
//     NewName = $("input[name=name]").val();
//     NewIntro = $("textarea[name=intro]").val();
//     NewProfileImage = $("input[name=profile_img]")[0].files[0];
//     CSRFToken = $("input[name=csrfmiddlewaretoken]").val();

//     data.append("identify", Username)
//     data.append("name", NewName)
//     data.append("intro", NewIntro)
//     data.append("profile_img", NewProfileImage)
//     data.append("csrfmiddlewaretoken", CSRFToken)

//     EditProfile(data);

// });

$(document).on("click", "#cancel-edit", function (e) {
    $(".profile-info").css("display", "block");
    $("#user-edit-form").css("display", "none");
});


// function EditProfile(data) {

//     $(".profile-info").remove();

//     $.ajax({
//         url: "/backend",
//         type: "POST",
//         mimeType: "multipart/form-data",
//         processData: false,
//         contentType: false,
//         data: data,
//         success: function (response) {
//             $("#user-edit-form").css("display", "none");
//             location.reload();
//         }
//     })
// }


//--------------------//
//  Popover           //
//--------------------//


// for popover
$(function () {
    $(".profile-popover").popover({
        html: true,
        content: function () {
            var content = $(this).attr("data-popover-content");
            return $(content).html();
        },
    });

});

$(function () {
    $(".notify-popover").popover({
        html: true,
        content: function () {
            var content = $(this).attr("data-popover-content");
            return $(content).html();
        },
    });
});


// dismiss when next click
$('.notify-popover').click(function (e) {
    ReadNotify();
    e.stopPropagation();
});

$('.profile-popover').click(function (e) {
    e.stopPropagation();
});


$(document).click(function (e) {
    if (($('.popover').has(e.target).length == 0)) {
        $('.notify-popover').popover('hide');
        $('.profile-popover').popover('hide');
    }
});





//--------------------//
//  Comment Section   //
//--------------------//

var NewOrReplyOrUpdate = "";
var CommentID = "";

$(document).on("click", ".comment-svg", function (e) {

    e.preventDefault();
    $(".popup-form").css("display", "block");
    ParentWidth = $(".popup-form").parent().css("width");
    $("#reply-form").css("width", ParentWidth);
    NewOrReplyOrUpdate = "New";

});

$(document).on("click", ".reply-btn", function (e) {

    e.preventDefault();
    $(".popup-form").css("display", "block");
    ParentWidth = $(".popup-form").parent().css("width");
    $("#reply-form").css("width", ParentWidth);
    NewOrReplyOrUpdate = "Reply";
    ClosestParent = $(this).closest(".parent-comment")
    ParentCommentID = ClosestParent.find("#comment-id").val();

});

$(document).on("click", ".new-reply-btn", function (e) {

    e.preventDefault();
    $(".popup-form").css("display", "block");
    ParentWidth = $(".popup-form").parent().css("width");
    $("#reply-form").css("width", ParentWidth);
    NewOrReplyOrUpdate = "New";

});


$(document).on("click", ".close-reply-form", function (e) {
    $(".popup-form").css("display", "none");
});


// #comment-dropdown-btn always happen before delete and edit
$(document).on("click", ".comment-dropdown-btn", function (e) {

    TargetComment = $(this).closest(".single-comment")

    // $.trim() equal to str.strip(), delete spaces.
    CommentBody = $.trim(TargetComment.find(".comment-body").text());
    CommentID = TargetComment.find("#comment-id").val();

});


$(document).on("click", "#delete-comment-btn", function (e) {
    e.preventDefault();
    $.ajax({
        url: "/delete_comment/" + CommentID,
        type: "DELETE",
        success: function () {

            // if TargetComment is a parent comment, remove children as well(whole comment-list).
            if (TargetComment.hasClass("child-comment") == true) {
                TargetComment = TargetComment;
            } else {
                TargetComment = TargetComment.parent();
            }

            $(TargetComment).remove();
            CurrentCommentsCount = Number($("#comments-count").text());
            $("#comments-count").text(CurrentCommentsCount - 1);

        }
    })
});

$(document).on("click", "#edit-comment", function (e) {

    e.preventDefault();
    NewOrReplyOrUpdate = "Update"

    $(".popup-form").css("display", "block");
    $(".popup-form").find("textarea[name=comment_body]").val(CommentBody);

    ParentWidth = $(".popup-form").parent().css("width");
    $("#reply-form").css("width", ParentWidth);
});


$(document).on("click", ".post-btn", function (e) {

    e.preventDefault();
    CSRFToken = $("input[name=csrfmiddlewaretoken]").val();
    CommentText = $("textarea[name=comment_body]").val();

    // Create New Comment
    if (NewOrReplyOrUpdate == "New") {

        // 1. New Parent Comment
        $.ajax({
            url: "/create_comment",
            type: "POST",
            data: {
                "new_reply_update": NewOrReplyOrUpdate,
                "post_id": PostID,
                "csrfmiddlewaretoken": CSRFToken,
                "comment_body": CommentText,
            },
            success: function (response) {
                $(".comments").append(response);
                CurrentCommentsCount = Number($("#comments-count").text());
                $("#comments-count").text(CurrentCommentsCount + 1);
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                alert("Status: " + textStatus + " | " + "Error: " + errorThrown);
            }

        })
    } else if (NewOrReplyOrUpdate == "Reply") {

        // 2. New Child Comment
        $.ajax({
            url: "/create_comment",
            type: "POST",
            data: {
                "parent_comment_id": ParentCommentID,
                "new_reply_update": NewOrReplyOrUpdate,
                "post_id": PostID,
                "csrfmiddlewaretoken": CSRFToken,
                "comment_body": CommentText,
            },
            success: function (response) {
                $(ClosestParent).append(response);
                CurrentCommentsCount = Number($("#comments-count").text());
                $("#comments-count").text(CurrentCommentsCount + 1);

            }
        })
    } else if (NewOrReplyOrUpdate == "Update") {

        // Update Comment
        $.ajax({
            url: "/update_comment/" + CommentID,
            type: "PUT",
            data: {
                "csrfmiddlewaretoken": CSRFToken,
                "comment_body": CommentText,
            },
            success: function (response) {
                $(TargetComment).html(response);

            }
        })

    } else {
        alert("something wrong.")
    }

    $("textarea[name=comment_body]").val("");
    $(".popup-form").css("display", "none");
});

function LikePost(identify) {
    $.ajax({
        url: "/like",
        type: "POST",
        data: {
            "post_or_comment": "Post",
            "identify": identify,
        },
        success: function (response) {

            Status = response.status;
            CurrentLike = Number($("#likes-count").text());

            if (Status == "success") {

                LikeOrUnlike = response.action;
                if (LikeOrUnlike === "Like") {

                    $("#post-like").css("fill", "var(--color-primary)");
                    $("#likes-count").text(CurrentLike + 1);

                } else if (LikeOrUnlike === "Unlike") {

                    $("#post-like").css("fill", "var(--color-muted)");
                    $("#likes-count").text(CurrentLike - 1);

                }
            } else {

                Action = response.action;
                if (Action == "RedirectLogIn") {
                    window.location.href = "/account/login";
                }
            }

        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            alert("Status: " + textStatus + " | " + "Error: " + errorThrown);
        }
    })
}


function LikeComment(identify) {
    $.ajax({
        url: "/like",
        type: "POST",
        data: {
            "post_or_comment": "Comment",
            "identify": identify,
        },
        success: function (response) {

            Status = response.status;
            LikesCountId = "#" + identify + "-likes-count";
            LikesSvgId = "#" + identify + "-comment-like";
            CurrentLike = Number($(LikesCountId).text());

            if (Status == "success") {

                LikeOrUnlike = response.action;
                if (LikeOrUnlike === "Like") {

                    $(LikesSvgId).css("fill", "var(--color-primary)");
                    $(LikesCountId).text(CurrentLike + 1);


                } else if (LikeOrUnlike === "Unlike") {

                    $(LikesSvgId).css("fill", "var(--color-muted)");
                    $(LikesCountId).text(CurrentLike - 1);

                }
            } else {

                Action = response.action;
                if (Action == "RedirectLogIn") {
                    window.location.href = "/account/login";
                }
            }

        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            alert("Status: " + textStatus + " | " + "Error: " + errorThrown);
        }
    })
}

// Like function
$(document).on("click", ".post-like-btn", function (e) {
    e.preventDefault();
    LikePost(PostID);
});


$(document).on("click", ".comment-like-btn", function (e) {

    e.preventDefault();
    PostOrComment = "Comment"
    CommentID = $(this).closest(".single-comment").find("input").val()
    LikeComment(CommentID);

});



function Bookmark(identify, BookmarkSvg) {
    $.ajax({
        url: "/bookmark",
        type: "POST",
        data: {
            "identify": identify,
        },
        success: function (response) {

            Status = response.status
            if (Status == "success") {
                AddOrDelete = response.action;
                if (AddOrDelete === "Add") {
                    BookmarkSvg.find("svg").css("fill", "var(--color-primary)");

                } else if (AddOrDelete === "Delete") {

                    BookmarkSvg.find("svg").css("fill", "var(--color-muted)");
                }

            } else {
                Action = response.action;
                if (Action == "RedirectLogIn") {
                    window.location.href = "/account/login";
                }
            }

        },
    })
}


// bookmark function
$(document).on("click", ".bookmark-btn", function (e) {

    e.preventDefault();
    Bookmark(PostID, $(this));
});



function ReadNotify() {
    $.ajax({
        url: "/notification/read_notify",
        type: "post",
        data: {
            "action": "read_notify",
        },
        success: function () {
        },
    })
}

// read notify function
$(document).on("click", "#notifications-tab", function (e) {
    ReadNotify();
});


$(document).on("click", ".post-likes-count-btn", function (e) {

    e.preventDefault();

    Target = "Post"
    ShowLikesList(PostID);

});

$(document).on("click", ".comment-likes-count-btn", function (e) {

    e.preventDefault();

    Target = "Comment"
    TargetComment = $(this).closest(".single-comment")
    CommentID = TargetComment.find("#comment-id").val();
    ShowLikesList(CommentID);

});


function ShowLikesList(identify) {
    $.ajax({
        url: "/show_liked_user",
        type: "POST",
        data: {
            "Target": Target,
            "identify": identify,
        },
        success: function (response) {
            $(".likes-list").empty();
            $(".likes-list").append(response);
            $("#likes-list").modal("show");
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            console.log(identify);
            alert("Status: " + textStatus + " | " + "Error: " + errorThrown);
        }
    })
}


$(document).on("click", "#save-post", function (e) {

    e.preventDefault();

    var data = new FormData();


    // for solving figure issue
    // there will be some default html tag added for figure.
    $('figure').each(function () {

        $(this).find('div').remove();
        $(this).find('figcaption').remove();
        $(this).removeClass('ck-widget ck-widget_with-resizer');

    })


    Body = $(".ck-editor__editable").html().replace(/<br\s*\\?>/g, "\n");
    CoverImage = $("input[name=cover_image]")[0].files[0];
    Description = $("textarea[name=description]").val();
    Status = $("select[name=status]").val();
    Title = $("input[name=title]").val();
    Tags = $("input[name=tags]").val();
    AuthorId = $("input[name=user_id]").val();
    CSRFToken = $("input[name=csrfmiddlewaretoken]").val();

    data.append("body", Body)
    data.append("cover_image", CoverImage)
    data.append("description", Description)
    data.append("status", Status)
    data.append("title", Title)
    data.append("tags", Tags)
    data.append("user_id", AuthorId)
    data.append("csrfmiddlewaretoken", CSRFToken)


    if (mode == "new") {
        CreateArticle(data);
    };

    if (mode == "update") {
        UpdateArticle(data);
    }

});

$(document).on("click", ".delete-post", function (e) {
    slug = $(this).closest('td').find('input').val();
});

$(document).on("click", ".delete-confirm", function (e) {
    DeleteArticle(slug);
});


function CreateArticle(data) {

    $.ajax({
        url: "/create_article",
        type: "POST",
        mimeType: "multipart/form-data",
        processData: false,
        contentType: false,
        data: data,
        dataType: "json",
        success: function (response) {

            if (response.status == 'success') {

                if (response.action == 'to_backend') {
                    window.location.replace("/stats");

                }

                if (response.action == 'to_article') {
                    slug = response.slug
                    window.location.replace("/a/" + slug);

                }
            }
        }
    })
}

function UpdateArticle(data) {

    $.ajax({
        url: "/update_article/" + slug,
        type: "POST",
        mimeType: "multipart/form-data",
        processData: false,
        contentType: false,
        data: data,
        dataType: "json",
        success: function (response) {

            if (response.status == 'success') {

                if (response.action == 'to_backend') {
                    window.location.replace("/stats");

                }

                if (response.action == 'to_article') {
                    slug = response.slug
                    window.location.replace("/a/" + slug);

                }
            }
        }
    })
}

function DeleteArticle(slug) {
    $.ajax({
        url: "/delete_article/" + slug,
        type: "DELETE",
        dataType: "json",
        success: function (response) {

            if (response.status == 'success') {

                window.location.replace("/stats");

            }
        }
    })
}


$(document).on("click", ".close-comment-form", function (e) {
    $(".popup-form").css("display", "none");
});


function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#cover-image-preview').attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]);
    }
}

$("#id_profile_img").change(function () {
    $('#user-edit-form').submit()
});

$("#id_cover_image").change(function () {
    readURL(this)
});

