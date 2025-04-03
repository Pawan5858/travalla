
var currAdminDetails = null;
// var currAdminConsoleType = getCurrAdminConsoleType();
// var currAdminConsoleType ='MAIN_ADMIN';
var currAdminConsoleType ='CLIENT_ADMIN';
var currentCityId = null
// var currentCityName = "Select City"
var currentCityName = localStorage.getItem('currentCityName') ? localStorage.getItem('currentCityName') : 'select city';

$(function () {
  formSubmit = true;
  currAdminDetails = JSON.parse(localStorage.getItem("adminDetails"))

  //$('#topStripCurrentUserName').text(currAdminDetails.firstname + (isInvalidString(currAdminDetails.lastname) ? '' : ' '+currAdminDetails.lastname) + ' ')
  $('#topStripCurrentUserName').text(currAdminDetails.username)

  $("#modal_conformation").modal({
    dismissible: false
  });
  
})

function openSubMenu(el) {
  if ($(el).parent().hasClass('menu-opt-li-open')) {
    $(el).parent().removeClass('menu-opt-li-open');
  } else {
    $('.menu-opt-li').removeClass('menu-opt-li-open');
    $(el).parent().addClass('menu-opt-li-open');
  }
  $('.submenu-opt-li').removeClass('submenu-opt-li-open');
}

function openInnerMenu(el) {
  // alert('inner')
  if ($(el).parent().hasClass('submenu-opt-li-open')) {
    $(el).parent().removeClass('submenu-opt-li-open');
  } else {
    $('.submenu-opt-li').removeClass('submenu-opt-li-open');
    $(el).parent().addClass('submenu-opt-li-open');
  }
}

function showToggleSearchBtn() {
  
  // $('.toggleSearchBtn').removeClass('d-none')
}

function toggleSearchContainer() {

  $('.pageHeaderContainer').toggleClass('d-none')
  $('.searchContainer').toggleClass('d-none')
}

function myProfileBtnAction() {

  setMyProfileData()
  $('#myProfileModal').modal("show")
}

function setMyProfileData() {

  var ele = '#myProfileModal '

  $(ele+'.firstName').text(getValidData_toDisplay(currAdminDetails.firstname))
  $(ele+'.lastName').text(getValidData_toDisplay(currAdminDetails.lastname))
  $(ele+'.email').text(getValidData_toDisplay(currAdminDetails.email))
  $(ele+'.mobileno').text(getValidData_toDisplay(currAdminDetails.mobileno))
  $(ele+'.desg').text(getValidData_toDisplay(currAdminDetails.desg))
  $(ele+'.role').text('-')
}

function changePwdBtnAction() {

  resetForm('#changePwdForm')

  $('#adminChangePwdModal').modal("show")
}

function adminChangePwdAction() {

  var formEle = '#changePwdForm'
  if (validateForm(formEle)) {

    var changePwdForm = document.getElementById("changePwdForm");
    var formData = new FormData(changePwdForm);

    formData.set('oldPwd', rsa_encrypt.encrypt(formData.get('oldPwd')));
    formData.set('newPwd', rsa_encrypt.encrypt(formData.get('newPwd')));

    console.log(currAdminConsoleType)
    console.log(adminConsoleTypesEnum.client_admin)
    
    $.ajax({
      url: baseUrl + (currAdminConsoleType==adminConsoleTypesEnum.client_admin ? 'admin/changePwd' : 'admin/mainAdminChangePwd'),
      data: formData,
      cache: false,
      processData: false,
      contentType: false,
      type: 'PATCH',
      success: function (result) {
        if (apiResStatus(result.status)) {

          $('#adminChangePwdModal').modal("hide")

          var userDetails = JSON.parse(localStorage.getItem("adminDetails"))
          userDetails.sessiontoken = result.sessiontoken
          
          if(currAdminConsoleType==adminConsoleTypesEnum.client_admin)
            addUserSession(userDetails)
          else
            addMainUserSession(userDetails)
        }
        show_StatusModal(result.message, result.status)
      },
      error: errorCallBack
    });
  }
}

function logoutBtnAction() {

  show_conformationModal({message: "Are you sure to logout."}, function(conformation) { 
    if (!conformation) return;

    $.ajax({
      url: baseUrl + (currAdminConsoleType==adminConsoleTypesEnum.client_admin ? 'admin/logout' : 'logout/'),
      type: "DELETE",
      contentType: "application/json",
      dataType: 'json',
      success: function (result) {

        if (apiResStatus(result.status)) {

          clearUserSession()
          window.location.href = "/login";

        } else {
          show_StatusModal(result.message, result.status)
        }
      },
      error: errorCallBack
    });
    
  })

}






