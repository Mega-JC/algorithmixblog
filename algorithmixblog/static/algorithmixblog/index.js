const setCookie = (cookieName, cookieValue, expirationDays) => {
  let d = new Date();
  d.setTime(d.getTime() + (expirationDays * 864* 100000));
  let expiry = "expires="+d.toUTCString();
  document.cookie = cookieName + "=" + cookieValue + ";" + expiry + ";path=/";
}
  
const getCookie = (cookieName) => {
  let name = cookieName + "=";
  let ca = document.cookie.split(';');
  for(let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
    c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}


const loadHeader = function () {
  const headerToggleButton = document.querySelector(".header-drawer-btn");
  const mainHeader = document.querySelector(".main-header");
  const headerClip = document.querySelector(".header-clip");
  const headerToggleIcon = document.querySelector(".header-drawer");

  let oldScrollY = window.scrollY;
  const oldTop = mainHeader.style.top;

  const headerToggle = function () {
    headerToggleButton.dataset.toggle = !headerToggleButton.dataset.toggle;
    mainHeader.classList.toggle("header-expand");
    headerClip.classList.toggle("header-expand");
    headerToggleIcon.classList.toggle("header-drawer-active");
  }
  
  const headerMinimize = function () {
    if (headerToggleButton.dataset.toggle) {
      headerToggleButton.dataset.toggle = false;
      mainHeader.classList.remove("header-expand");
      headerClip.classList.remove("header-expand");
      headerToggleIcon.classList.remove("header-drawer-active");
    }
  }
  
  window.onscroll = () => {
    if ( window.scrollY > 50 && window.scrollY > oldScrollY ) {
      mainHeader.style.top =  "-100px";
      headerMinimize();  
    } else {
      mainHeader.style.top = oldTop;
    }
    oldScrollY = window.scrollY;
  }

  window.onresize = () => {
    if (window.innerWidth > 700  && parseInt(headerToggleButton.dataset.toggle) ) {
      headerToggleButton.dataset.toggle = false;
      mainHeader.classList.remove("header-expand");
      headerClip.classList.remove("header-expand");
      headerToggleIcon.classList.remove("header-drawer-active");
    };  
  };

  headerToggleButton.onclick = headerToggle;
};

const createHTMLUserPreview = (userPreviewObj) => {
  const userInfoCellTemplate = document.querySelector("#user-info-cell-template");
  const userInfoCell = userInfoCellTemplate.content.firstElementChild.cloneNode(true);

  const userInfoCellLink = userInfoCell.querySelector(".link");

  userInfoCellLink.setAttribute("href", `/user/${userPreviewObj.id}`);

  const userInfoCellTitle = userInfoCell.querySelector(".title");
  userInfoCellTitle.innerText = userPreviewObj.username;
  const userInfoCellCreated = userInfoCell.querySelector(".created");
  userInfoCellCreated.innerText = userPreviewObj.created.ftimestamp;
  const userInfoCellID = userInfoCell.querySelector(".id");
  userInfoCellID.innerText = userPreviewObj.id;

  const userInfoCellFollowerCount = userInfoCell.querySelector(".followers .count");
  userInfoCellFollowerCount.innerText = userPreviewObj.follower_count;

  const userInfoCellFollowingCount = userInfoCell.querySelector(".following .count");
  userInfoCellFollowingCount.innerText = userPreviewObj.following_count;

  if (userPreviewObj.bio) {
    const userInfoCellBio = userInfoCell.querySelector(".bio");
    userInfoCellBio.innerText = (userPreviewObj.bio.length > 128 ? userPreviewObj.bio.substring(0, 128) + "... (view profile for more)" : userPreviewObj.bio);
  } else {
    userInfoCell.removeChild(userInfoCell.querySelector(".bio"));
  }

  return userInfoCell;
}

const createHTMLBlogPostPreview = (bpPreviewObj, pageType) => {

  const bpPreviewCellTemplate = document.querySelector("#bp-prev-cell-template");
  const bpPreviewCell = bpPreviewCellTemplate.content.firstElementChild.cloneNode(true);

  bpPreviewCell.className = "bp-prev-cell";
  switch (pageType) {
    case "home":
      bpPreviewCell.classList.add("homepage-wh");
      break;

    case "discover":
      const randVal = Math.random();
      if (randVal < 0.25) {
        bpPreviewCell.classList.add("large-wh")
      }
      else if (randVal < 0.5) {
        bpPreviewCell.classList.add("large-h")
      }

      else if (randVal < 0.75) {
        bpPreviewCell.classList.add("large-w")
      }
      break;

    case "userprofile":
      bpPreviewCell.classList.add("homepage-wh");
      break;
  }

  if (bpPreviewObj.is_private) {
    bpPreviewCell.classList.add("private");
  }

  const linkWrapper = bpPreviewCell.querySelector("a");
  linkWrapper.setAttribute("href", `/blogpost/${bpPreviewObj.id}`)
  //linkWrapper.setAttribute("href", "#");

  const bpPreviewCellTitle = bpPreviewCell.querySelector(".title");
  bpPreviewCellTitle.innerText = bpPreviewObj.title;

  const bpPreviewCellLikeInfo = bpPreviewCell.querySelector(".like-info");

  const bpPreviewCellLikeCount = bpPreviewCellLikeInfo.querySelector(".count");
  bpPreviewCellLikeCount.innerText = bpPreviewObj.like_count;

  const bpPreviewCellCommentInfo = bpPreviewCell.querySelector(".comment-info");

  const bpPreviewCellCommentCount = bpPreviewCellCommentInfo.querySelector(".count");
  bpPreviewCellCommentCount.innerText = bpPreviewObj.comment_count;

  const bpPreviewCellPostInfo = bpPreviewCell.querySelector(".post-info");
  const bpPreviewCellPostDate = bpPreviewCellPostInfo.querySelector(".date");
  const bpPreviewCellPostAuthorUserLink = bpPreviewCellPostInfo.querySelector("a");
  const bpPreviewCellPostAuthorUserName = bpPreviewCellPostInfo.querySelector(".username");

  bpPreviewCellPostDate.innerText = bpPreviewObj.created.ftimestamp;
  bpPreviewCellPostAuthorUserLink.setAttribute("href", `/user/${bpPreviewObj.author.id}`);
  bpPreviewCellPostAuthorUserName.innerText = bpPreviewObj.author.username;

  if (bpPreviewObj.request_user_id === bpPreviewObj.author.id) {
    bpPreviewCell.classList.add("your-post");
    const bpPreviewCellVisibilityInfo = document.createElement("span");
    bpPreviewCellVisibilityInfo.classList.add("visibility");
    bpPreviewCellVisibilityInfo.innerText = (bpPreviewObj.is_private ? "Visibility: Private 🔐": "Visibility: Public 🌎");
    bpPreviewCellPostInfo.append(document.createElement("br"), bpPreviewCellVisibilityInfo);
  }

  const bpPreviewCellCover = bpPreviewCell.querySelector(".cover");
  let bpPreviewCellCoverImg = null;

  if (bpPreviewObj.cover_url) {
    bpPreviewCellCoverImg = document.createElement("img");
    bpPreviewCellCoverImg.className = "cover-img";
    bpPreviewCellCoverImg.setAttribute("src", bpPreviewObj.cover_url);
    bpPreviewCellCoverImg.setAttribute("alt", "cover");

    if (bpPreviewCell.classList.contains("large-wh") || bpPreviewCell.classList.contains("large-h")) {
      bpPreviewCellCoverImg.style.height = "100%";
      bpPreviewCellCoverImg.style.width = "unset";
    } else {
      bpPreviewCellCoverImg.style.height = "unset";
      bpPreviewCellCoverImg.style.width = "100%";
    }
  }

  if (bpPreviewCellCoverImg !== null) {
    bpPreviewCellCover.append(bpPreviewCellCoverImg);
  };

  bpPreviewCell.addEventListener("mouseenter", () => {
    bpPreviewCellCover.classList.add("fadeout");
  });

  bpPreviewCell.addEventListener("touchenter", () => {
    bpPreviewCellCover.classList.add("fadeout");
  });

  bpPreviewCell.addEventListener("mouseleave", () => {
    bpPreviewCellCover.classList.remove("fadeout");
  });

  bpPreviewCell.addEventListener("touchleave", () => {
    bpPreviewCellCover.classList.remove("fadeout");
  });

  const bpPreviewCellPreviewText = bpPreviewCell.querySelector(".preview-text");
  bpPreviewCellPreviewText.className = (pageType === "discover" ? "preview-text": "preview-text-small");

  bpPreviewCellPreviewText.innerText = bpPreviewObj.description;

  return bpPreviewCell;
};

const loadHomePageWidgetPosts = (homePageWidget) => {

  let counter = parseInt(homePageWidget.dataset.counter);
  let quantity = parseInt(homePageWidget.dataset.quantity);

  let start = counter;
  let end = start + quantity;
  counter = end;

  homePageWidget.dataset.counter = counter;

  fetch(`blogpostspreview?sort=${homePageWidget.dataset.sort}&start=${start}&end=${end}`)
  .then(request => request.json())
  .then(blogPostPreviews => {
    for (const blogPostPreview of blogPostPreviews) {
      homePageWidget.append(createHTMLBlogPostPreview(blogPostPreview, "home"));  
    };
  });
};

const loadHomePage = () => {
  const homePageWidgets = document.querySelector("#homepage-widgets");
  if (homePageWidgets !== null) {
    Array.from(homePageWidgets.children).forEach(
      homePageWidgetWrapper => {   
        const homePageWidgetHead = homePageWidgetWrapper.querySelector(".homepage-widget-head");
        const homePageWidget = homePageWidgetWrapper.querySelector(".homepage-widget");
        const homePageWidgetToggleBtn = homePageWidgetHead.querySelector(".homepage-widget-toggle-btn");
        const homePageWidgetToggleIcon = homePageWidgetToggleBtn.querySelector(".homepage-widget-toggle");
        
        loadHomePageWidgetPosts(homePageWidget);
        homePageWidget.onscroll = () => {
          if (homePageWidget.scrollHeight - homePageWidget.scrollTop - homePageWidget.clientHeight < 1) {
            loadHomePageWidgetPosts(homePageWidget);
          }
        };

        homePageWidgetToggleBtn.onclick = () => {
          homePageWidgetToggleIcon.classList.toggle("homepage-widget-toggle-active");
          homePageWidget.classList.toggle("closed");
          homePageWidgetHead.classList.toggle("closed");
        };

        Array.from(homePageWidget.children).forEach(
          child => {      
            const cellCover = child.querySelector(".cover");
      
            child.addEventListener("mouseenter", () => {
              cellCover.classList.add("fadeout");
            });
      
            child.addEventListener("touchenter", () => {
              cellCover.classList.add("fadeout");
            });
      
            child.addEventListener("mouseleave", () => {
              cellCover.classList.remove("fadeout");
            });
      
            child.addEventListener("touchleave", () => {
              cellCover.classList.remove("fadeout");
            });
          }
        );
      }
    );
  };
}

const loadDiscoverPagePosts = (discoverContainer) => {

  let counter = parseInt(discoverContainer.dataset.counter);
  let quantity = parseInt(discoverContainer.dataset.quantity);

  let start = counter;
  let end = start + quantity;
  counter = end;

  discoverContainer.dataset.counter = counter;

  fetch(`blogpostspreview?sort=${discoverContainer.dataset.sort}&start=${start}&end=${end}`)
  .then(request => request.json())
  .then(blogPostPreviews => {
    for (const blogPostPreview of blogPostPreviews) {
      discoverContainer.append(createHTMLBlogPostPreview(blogPostPreview, "discover"));  
    };
  });
};


const loadDiscoverPage = () => {
  const discoverContainer = document.querySelector("#discover-container");
  if (discoverContainer !== null) {
    
    loadDiscoverPagePosts(discoverContainer);
    window.onscroll = () => {
      if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
        loadDiscoverPagePosts(discoverContainer);
      }
    };
    
    Array.from(discoverContainer.children).forEach(
      child => {      
        const cellCover = child.querySelector(".cover");

        child.addEventListener("mouseenter", function( event ) {
          cellCover.classList.add("fadeout");
        });

        child.addEventListener("touchenter", function( event ) {
          cellCover.classList.add("fadeout");
        });

        child.addEventListener("mouseleave", function( event ) {
          cellCover.classList.remove("fadeout");
        });

        child.addEventListener("touchleave", function( event ) {
          cellCover.classList.remove("fadeout");
        });

      }
    );
  }
}


const loadSearchPage = () => {
  const searchResultsContainer = document.querySelector("#search-results-container");
  if (searchResultsContainer !== null) {
    Array.from(searchResultsContainer.children).forEach(
      child => {      
        const cellCover = child.querySelector(".cover");
  
        child.addEventListener("mouseenter", () => {
          cellCover.classList.add("fadeout");
        });
  
        child.addEventListener("touchenter", () => {
          cellCover.classList.add("fadeout");
        });
  
        child.addEventListener("mouseleave", () => {
          cellCover.classList.remove("fadeout");
        });
  
        child.addEventListener("touchleave", () => {
          cellCover.classList.remove("fadeout");
        });
      }
    );
  }
};


const loadPostPage = () => {

  const csrfToken = getCookie("csrftoken");
  const bpLikeBtn = document.querySelector("#post-options .post-like-btn");
  const bpFavoritesBtn = document.querySelector(".favorites-btn");
  const bpVisibilityBtn = document.querySelector("#post-options .visibility-btn");
  const bpDeleteBtn = document.querySelector("#post-options .delete-btn");

  
  if (bpLikeBtn !== null) {
    const bpLikeCount = bpLikeBtn.querySelector(".count");
    bpLikeBtn.onclick = (event) => {
      const toggle = parseInt(bpLikeBtn.dataset.toggle);
  
      fetch(`/${parseInt(bpLikeBtn.dataset.blogpost_id)}/toggleblogpostlike`, {
        method: "PUT",
        credentials: "include",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=UTF-8',
            'X-CSRFToken': csrfToken
          },
        body: JSON.stringify({
            value: (toggle ? false : true)
        })
      });
  
      bpLikeCount.innerText = parseInt(bpLikeCount.innerText) + (toggle ? -1 : 1);
      bpLikeBtn.dataset.toggle = 1-toggle;
      bpLikeBtn.classList.toggle("liked");
    };
  }
  
  if (bpFavoritesBtn !== null) {
    bpFavoritesBtn.onclick = (event) => {
      const toggle = parseInt(bpFavoritesBtn.dataset.toggle);
  
      fetch(`/${parseInt(bpFavoritesBtn.dataset.blogpost_id)}/toggleblogpostfavorites`, {
        method: "PUT",
        credentials: "include",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=UTF-8',
            'X-CSRFToken': csrfToken
          },
        body: JSON.stringify({
            value: (toggle ? false : true)
        })
      });
  
      bpFavoritesBtn.innerText = (toggle ? "Add Favorite ⭐" : "Remove Favorite ❌");
      bpFavoritesBtn.dataset.toggle = 1-toggle;
      bpFavoritesBtn.classList.toggle("favorited");
    };
  }
  
  if (bpVisibilityBtn !== null) {
    bpVisibilityBtn.onclick = (event) => {
      const toggle = parseInt(bpVisibilityBtn.dataset.toggle);
  
      fetch(`/${parseInt(bpVisibilityBtn.dataset.blogpost_id)}/toggleblogpostvisibility`, {
        method: "PUT",
        credentials: "include",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=UTF-8',
            'X-CSRFToken': csrfToken
          },
        body: JSON.stringify({
            value: (toggle ? false : true)
        })
      });
  
      bpVisibilityBtn.innerText = (toggle ? "Make Private 🔐" : "Make Public 🌎");
      bpVisibilityBtn.dataset.toggle = 1-toggle;
      bpVisibilityBtn.classList.toggle("private");
    };
  }

  if (bpDeleteBtn !== null) {
    bpDeleteBtn.onclick = () => {
      if (confirm("Are you sure you want to delete this blog post and all its likes and comments?")) {
        fetch(`/${parseInt(bpDeleteBtn.dataset.blogpost_id)}/blogpostdelete`, {
          method: "DELETE",
          credentials: "include",
          headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json; charset=UTF-8',
              'X-CSRFToken': csrfToken
            }
        });

        location.href = "/";
      }
    }
  }

  const bpBodyText = document.querySelector("#post-wrapper .text");

  if (bpBodyText !== null) {
    const pTags = bpBodyText.querySelectorAll("p");

    if (pTags !== null) {
      for (let pTag of pTags) {
        if (pTag.children.length === 1 && pTag.children[0].nodeName === "IMG") {

          const img  = pTag.children[0];
          
          const imgFigure = document.createElement("figure");
          const imgFigCaption = document.createElement("figcaption");

          imgFigure.classList.add("img-figure");
          pTag.insertBefore(imgFigure, img);
          imgFigCaption.innerText = img.title;
          imgFigure.append(img, imgFigCaption);

        }
        else if (pTag.children.length > 1 && Array.from(pTag.children).every((elem) => elem.nodeName === "IMG")) {
          
          const imgContainer = document.createElement("div");
          imgContainer.classList.add("img-container");

          const imgs = pTag.children;

          for (let img of imgs) {
            const imgFigure = document.createElement("figure");
            const imgFigCaption = document.createElement("figcaption");
            imgFigure.classList.add("img-figure");
            pTag.insertBefore(imgFigure, img);
            imgFigCaption.innerText = img.title;
            imgFigure.append(img, imgFigCaption);
          }
          
          pTag.replaceWith(imgContainer);
          imgContainer.append(...imgs);

        }

        if (pTag.children.length >= 1) {
          const text = pTag.querySelector("text");
          if (text !== null) {
            pTag.textContent = text.innerText;
          }
        }
      }
    }

    const tableTags = bpBodyText.querySelectorAll("table");

    if (tableTags !== null) {
      for (const tableTag of tableTags) {
        const tableWrapper = document.createElement("div");
        tableWrapper.classList.add("table-wrapper");
    
        bpBodyText.insertBefore(tableWrapper, tableTag);
        tableWrapper.appendChild(tableTag);
      }
    }

    const bqSpoilerTags = bpBodyText.querySelectorAll("blockquote.spoiler");

    if (bqSpoilerTags !== null) {
      for (const bqSpoilerTag of bqSpoilerTags) {
        bqSpoilerTag.onclick = () => {
          bqSpoilerTag.classList.remove("spoiler")
        }
      }
    }

    const bpCommentContainer = document.querySelector("#comment-container");

    if (bpCommentContainer !== null) {
      
      const commentSectionTitle = document.querySelector("#comment-section-title");
      const commentForm = document.querySelector("#comment-form");


      if (commentForm !== null) {
        const commentFormTitle = commentForm.querySelector(".title");
        const commentTextArea = commentForm.querySelector(".input-textarea");
        const commentTextAreaCharCount = commentForm.querySelector(".char-count");
        const commentMode = commentForm.querySelector("#comment-mode");
        const submitCommentBtn = commentForm.querySelector("#submit-comment-btn");
        
        const showCharCountRemaining = (event) => {
          commentTextAreaCharCount.innerText = `(${4096-commentTextArea.value.length} characters remaining)`;
        }; 

        showCharCountRemaining();
        commentTextArea.addEventListener("input", showCharCountRemaining);
        commentTextArea.addEventListener("onfocus", showCharCountRemaining);
        commentTextArea.addEventListener("onmouseenter", showCharCountRemaining);

        for (const bpCommentWrapper of bpCommentContainer.children) {
          const likeBtn = bpCommentWrapper.querySelector(".like-btn");
          const likeCount = likeBtn.querySelector(".count");
          const editBtn = bpCommentWrapper.querySelector(".edit-btn");
          const replyBtn = bpCommentWrapper.querySelector(".reply-btn");
          const deleteBtn = bpCommentWrapper.querySelector(".delete-btn");

          likeBtn.onclick = (event) => {
            const toggle = parseInt(likeBtn.dataset.toggle);

            fetch(`/toggleblogpostcommentlike/${parseInt(likeBtn.dataset.comment_id)}`, {
              method: "PUT",
              credentials: "include",
              headers: {
                  'Accept': 'application/json',
                  'Content-Type': 'application/json; charset=UTF-8',
                  'X-CSRFToken': csrfToken
                },
              body: JSON.stringify({
                  value: (toggle ? false : true)
              })
            });

            likeCount.innerText = parseInt(likeCount.innerText) + (toggle ? -1 : 1);
            likeBtn.dataset.toggle = 1-toggle;
            likeBtn.classList.toggle("liked");
          }

          if (deleteBtn !== null) {
            deleteBtn.onclick = (event) => {
              if (confirm("Are you sure you want to delete this comment?")) {
                fetch(`/blogpostcommentdelete/${parseInt(deleteBtn.dataset.comment_id)}`, {
                  method: "DELETE",
                  credentials: "include",
                  headers: {
                      'Accept': 'application/json',
                      'Content-Type': 'application/json; charset=UTF-8',
                      'X-CSRFToken': csrfToken
                    }
                });


                bpCommentWrapper.classList.add("deletion");
                setTimeout(() => {
                  bpCommentContainer.removeChild(bpCommentWrapper);
                  commentSectionTitle.innerText = `Comments: ${bpCommentContainer.children.length}`;
                }, 500);
              }
            } 
          }

          if (editBtn !== null) {
            editBtn.onclick = (event) => {
              const toggle = parseInt(editBtn.dataset.toggle);
              if (toggle) {

                if (deleteBtn !== null) {
                  deleteBtn.style.display = "inline-block";
                }

                if (replyBtn !== null) {
                  replyBtn.style.display = "inline-block";
                }
                
                editBtn.innerText = "Edit";
                commentFormTitle.innerText = "Add New Comment";
                commentMode.name = "create";
                commentMode.value = "";
                bpCommentWrapper.classList.remove("editing");
                submitCommentBtn.innerText = "New Comment";
                commentTextArea.value = "";
    
                editBtn.dataset.toggle = 1-toggle;
              } else {
                if (!commentMode.value || parseInt(commentMode.value) === parseInt(editBtn.dataset.comment_id)) {
                  commentSectionTitle.scrollIntoView();
                  if (deleteBtn !== null) {
                    deleteBtn.style.display = "none";
                  }

                  if (replyBtn !== null) {
                    replyBtn.style.display = "none";
                  }
                  fetch(`/getblogpostcomment/${parseInt(editBtn.dataset.comment_id)}`)
                  .then(request => request.json())
                  .then(bpCommentData => {
                    if ("error" in bpCommentData) {
                      alert(bpCommentData.error);
                      editBtn.dataset.toggle = toggle;
                      location.reload();
                      return
                    } else {
                      editBtn.innerText = "Cancel";
                      commentFormTitle.innerText = "Edit Comment";
                      commentMode.name = "edit";
                      commentMode.value = parseInt(editBtn.dataset.comment_id);
                      bpCommentWrapper.classList.add("editing");
                      submitCommentBtn.innerText = "Edit Comment";
                      commentTextArea.value = bpCommentData.text;
                      showCharCountRemaining();
                      editBtn.dataset.toggle = 1-toggle;
                    }
                  });
                }
              }
              showCharCountRemaining();
            }
          }

          if (replyBtn !== null) {
            replyBtn.onclick = (event) => {
              const toggle = parseInt(replyBtn.dataset.toggle);
              if (toggle) {
                if (deleteBtn !== null) {
                  deleteBtn.style.display = "inline-block";
                }

                if (editBtn !== null) {
                  editBtn.style.display = "inline-block";
                }

                replyBtn.innerText = "Reply";
                commentFormTitle.innerText = "Add New Comment";
                commentMode.name = "create";
                commentMode.value = "";
                bpCommentWrapper.classList.remove("replying");
                submitCommentBtn.innerText = "New Comment";
                commentTextArea.value = "";
    
                replyBtn.dataset.toggle = 1-toggle;
              } else {
                if (!commentMode.value || parseInt(commentMode.value) === parseInt(replyBtn.dataset.comment_id)) {
                  commentSectionTitle.scrollIntoView();
                  
                  if (deleteBtn !== null) {
                    deleteBtn.style.display = "none";
                  }

                  if (editBtn !== null) {
                    editBtn.style.display = "none";
                  }

                  replyBtn.innerText = "Cancel Reply";
                  commentFormTitle.innerText = "Add New Reply Comment";
                  commentMode.name = "reply";
                  commentMode.value = parseInt(replyBtn.dataset.comment_id);
                  bpCommentWrapper.classList.add("replying");
                  replyBtn.dataset.toggle = 1-toggle;
                }
              }
            }
          }
        }
      }
    }
  }    
};

const loadFeedPage = () => {
  const feedPostContainer = document.querySelector(".feed-posts-container");

  if (feedPostContainer !== null) {
    Array.from(feedPostContainer.children).forEach(
      child => {      
        const cellCover = child.querySelector(".cover");

        child.addEventListener("mouseenter", function( event ) {
          cellCover.classList.add("fadeout");
        });

        child.addEventListener("touchenter", function( event ) {
          cellCover.classList.add("fadeout");
        });

        child.addEventListener("mouseleave", function( event ) {
          cellCover.classList.remove("fadeout");
        });

        child.addEventListener("touchleave", function( event ) {
          cellCover.classList.remove("fadeout");
        });

      }
    );
  }

};

const loadUserProfilePagePosts = (userPostContainer) => {

  let counter = parseInt(userPostContainer.dataset.counter);
  let quantity = parseInt(userPostContainer.dataset.quantity);

  let start = counter;
  let end = start + quantity;
  counter = end;

  userPostContainer.dataset.counter = counter;

  fetch(`/blogpostspreview?sort=${userPostContainer.dataset.sort}&user=${userPostContainer.dataset.user_id}&publiconly=${userPostContainer.dataset.publiconly}&start=${start}&end=${end}`)
  .then(request => request.json())
  .then(blogPostPreviews => {
    for (const blogPostPreview of blogPostPreviews) {
      userPostContainer.append(createHTMLBlogPostPreview(blogPostPreview, "userprofile"));
    };
  });
};

const loadUserFollowPageUsers = (userCellContainer) => {

  let counter = parseInt(userCellContainer.dataset.counter);
  let quantity = parseInt(userCellContainer.dataset.quantity);

  let start = counter;
  let end = start + quantity;
  counter = end;

  userCellContainer.dataset.counter = counter;

  fetch(`/userspreview?view_mode=${userCellContainer.dataset.view_mode}&target_user=${userCellContainer.dataset.user_id}&start=${start}&end=${end}`)
  .then(request => request.json())
  .then(userPreviews => {
    for (const userPreview of userPreviews) {
      userCellContainer.append(createHTMLUserPreview(userPreview));
    };
  });
};


const loadUserProfilePage = () => {
  const csrfToken = getCookie("csrftoken");

  const pathNameParts = window.location.pathname.split("/");
  const lastPathNamePage = pathNameParts[pathNameParts.length-1];
  if (lastPathNamePage === "followers" || lastPathNamePage === "following") {

    const userCellContainer = document.querySelector("#user-cell-container");
    loadUserFollowPageUsers(userCellContainer);

    window.onscroll = () => {
      if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
        loadUserFollowPageUsers(userCellContainer);
      }
    };

  } else {
    const userInfoPostContainer = document.querySelector("#user-info-container");
    const constUserFollowersCount = userInfoPostContainer.querySelector(".followers .count");
    const constUserFollowingsCount = userInfoPostContainer.querySelector(".following .count");
    const editInfoForm = userInfoPostContainer.querySelector("#edit-info-form");
    const sortUserBlogPostSelect = document.querySelector("#sort-user-bp-select");
    const followBtn = userInfoPostContainer.querySelector("#profile-options .follow-btn");

    if (followBtn !== null) {
      followBtn.onclick = (event) => {
        const toggle = parseInt(followBtn.dataset.toggle);
    
        fetch(`/${parseInt(followBtn.dataset.user_id)}/togglefollowuser`, {
          method: "PUT",
          credentials: "include",
          headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json; charset=UTF-8',
              'X-CSRFToken': csrfToken
            },
          body: JSON.stringify({
              value: (toggle ? false : true)
          })
        });
    
        constUserFollowersCount.innerText = parseInt(constUserFollowersCount.innerText) + (toggle ? -1 : 1);
        followBtn.innerText = (toggle ? "Follow" : "Unfollow");
        followBtn.dataset.toggle = 1-toggle;
        followBtn.classList.toggle("followed");
      };
    };

    if (editInfoForm !== null) {
      const editBioBtn = userInfoPostContainer.querySelector("#profile-options .edit-bio-btn");

        editBioBtn.onclick = (event) => {
          const toggle = parseInt(editBioBtn.dataset.toggle);
          if (toggle) {
            editInfoForm.style.display = "none";
            editBioBtn.innerText = "Edit Your Info";
          } else {
            editInfoForm.style.display = "";
            editBioBtn.innerText = "Cancel";
          }

          editBioBtn.dataset.toggle = 1-toggle;
        }

        const deleteUserBtn = userInfoPostContainer.querySelector("#profile-options .delete-user-btn");
        if (deleteUserBtn !== null) {
          deleteUserBtn.onclick = (event) => {
            if (confirm("Are you sure you want to delete this account? All blog posts and their comments created by this account will be permanently deleted!")) {
              fetch(`/${parseInt(deleteUserBtn.dataset.user_id)}/deleteuser`, {
                method: "DELETE",
                credentials: "include",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json; charset=UTF-8',
                    'X-CSRFToken': csrfToken
                  }
              });
              window.location = "/";
            }
          } 
        }
    };
    
    const userPostContainer = document.querySelector("#user-post-container");

    if (userPostContainer !== null) {
      if (sortUserBlogPostSelect !== null) {
        sortUserBlogPostSelect.addEventListener("change", (event) => {
          userPostContainer.dataset.sort = event.target.value;
          while (userPostContainer.lastChild) {
            userPostContainer.removeChild(userPostContainer.lastChild);
          }
          userPostContainer.dataset.counter = 0;
          loadUserProfilePagePosts(userPostContainer);
        });
      }
      

      loadUserProfilePagePosts(userPostContainer);
      window.onscroll = () => {
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
          loadUserProfilePagePosts(userPostContainer);
        }
      };

      Array.from(userPostContainer.children).forEach(
        child => {      
          const cellCover = child.querySelector(".cover");
    
          child.addEventListener("mouseenter", function( event ) {
            cellCover.classList.add("fadeout");
          });
    
          child.addEventListener("touchenter", function( event ) {
            cellCover.classList.add("fadeout");
          });
    
          child.addEventListener("mouseleave", function( event ) {
            cellCover.classList.remove("fadeout");
          });
    
          child.addEventListener("touchleave", function( event ) {
            cellCover.classList.remove("fadeout");
          });
    
        }
      );
    }  
  }
};

document.addEventListener("DOMContentLoaded", () => {
  loadHeader();
  switch ("/" + window.location.pathname.split("/", 2)[1]) {
    case "/discover":
      loadDiscoverPage();
      break;

    case "/search":
      loadSearchPage();
      break;

    case "/blogpost":
      loadPostPage();
      break;

      case "/feed":
        loadFeedPage();
        break;

      case "/user":
        loadUserProfilePage();
        break;
  
    default:
      loadHomePage();
      break;
  }
});