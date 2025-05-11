var packageData = null;
var ItineraryList = []

$(function () {
  formSubmit = true;
  showToggleSearchBtn();
  $('select').formSelect();
  
  fill_dataTable();

  $('.stateDate, .endDate, .itrldate').bsdatepicker({
    format: dateformat_type.DisplayDate_Small,
    autoclose: true
  }).on('changeDate', function (e) {
      $(this).parent().find('.datePicker i').removeClass('fa-calendar-alt').addClass('fa-calendar-times');
  });

})


function userPktSelected(ele){
  var val =$(ele).val()
  if(val=='ITINERARY'){
    $(".itineraryDiv").removeClass('d-none')
  }else{
    $(".itineraryDiv").addClass('d-none')
  }
}

function confirmDialog_Actions() {

  $('[data-toggle=confirmation]').confirmation({
    rootSelector: '[data-toggle=confirmation]',
    onConfirm: function () {
      var id = $(this).parents('tr').data('id');
      var status = $(this).data('value');

      switch (status) {
        case 'AC':
          updateStatusAction(id, 'NA');
          break;
        case 'NA':
          updateStatusAction(id, 'AC');
          break;
      }
    },
    onCancel: function () {
    }
  });

}

function fill_dataTable() {

  var table = $('#table_content').DataTable({
    "drawCallback": function (settings) {

      confirmDialog_Actions();

    },
    "fnRowCallback": function (nRow, aData, iDisplayIndex) {
      var oSettings = this.fnSettings();
      $("td:first", nRow).html(oSettings._iDisplayStart + iDisplayIndex + 1);
      return nRow;
    },
    "bLengthChange": false,
    "processing": true,
    "serverSide": true,
    "ajax": {
      "url": baseUrl+ "tour/packages_tabledata?datatable=true",
      "type": "POST",
      "dataFilter": function (reps) {
        packageData = JSON.parse(reps);
        return reps;
      }
    },
    createdRow: function (row, data, dataIndex) {
      $(row).data('id', data.torp_id);
    },
    "columnDefs": [
      {
        "targets": '_all',
        "render":$.fn.dataTable.render.text()
      },
      {
        'targets': [6], /* column index */
        'orderable': false, /* true or false */
      }
    ],
    "columns": [
      { 
        "data": "torp_id",
        "render": $.fn.dataTable.render.text()
      },
      { 
        "data": "torp_name",
        "render": $.fn.dataTable.render.text()
      },
      { 
        "data": "torp_package_type",
        "render": $.fn.dataTable.render.text()
      },
      { 
        "data": "torp_price",
        "render": $.fn.dataTable.render.text()
      },
      { 
        "data": "torp_destination",
        "render": $.fn.dataTable.render.text()
      },
      {
        "data": "torp_start_date",
        render: function (data) {
          return $.fn.dataTable.render.text().display(convertDateFormater(data, dateformat_type.ServerDate, dateformat_type.DayMonthYear));
        }
      },
      {
        "data": "torp_end_date",
        render: function (data) {
          return $.fn.dataTable.render.text().display(convertDateFormater(data, dateformat_type.ServerDate, dateformat_type.DayMonthYear));
        }
      },
      {
        "data": "torp_status",
        render: function (data) {
          var btn_type = (data === 'AC') ? 'btn-success' : 'btn-danger';
          var status = (data === 'AC') ? 'Active' : 'Not Active';

          return $('<div>').append($('<button />')
            .prop('type', 'button')
            .prop('class', 'btn ' + btn_type + ' btn_cstm_status')
            .css('width', '90px')
            .attr('data-value', data)
            .attr('data-toggle', 'confirmation')
            .attr('data-popout', 'true')
            .attr('data-singleton', 'true')
            .attr('data-btn-ok-label', 'Yes')
            .attr('data-btn-cancel-label', 'No')
            .attr('data-title', 'Change circle status')
            .text(status)).html();

        }
      },
      {
        "class": "text-center",
        "data": null,
        "render": function (data, type, row) {
          return `<a class="btn-floating btn-small waves-effect waves-light editbtn editEventTD" onclick="centerEditAction(this)"><i class="material-icons">edit</i></a>
                  <a class="btn-floating btn-small waves-effect waves-light deletebtn editEventTD" onclick="centerDeleteAction(this)"><i class="material-icons">delete</i></a>`;
        }
      }
    ]
  });

}


$('#table_content tbody').on('click', 'tr td:nth-child(n+1):nth-last-child(n+3)', function () {
  centerEditAction(this, forView = true);
});

function clearSearchAction() {

  $('.searchContainer input').val('');
  $('.searchContainer select').val('');
  $('.searchContainer .search_date .datePicker i').removeClass('fa-calendar-times').addClass('fa-calendar-alt');
  
  $('#table_content').DataTable().search('').columns().search('').draw();
}

function searchAction() {

  var table = $('#table_content').DataTable();

  table.columns(0).search($('.table_search_ps').val())
  table.columns(1).search($('.table_search_name').val())
  table.columns(2).search($('.table_search_dept').val())
  table.columns(3).search($('.table_search_incharge').val())
  table.columns(4).search($('.table_search_status').val())
  table.columns(5).search($('.table_search_subdivision').val())

  table.draw();
}

function invokeAddStdRouteBtnAction() {

  var formEle = '#stdRouteForm';

  $(formEle).removeClass('viewOnly')
  $('.subDivisionModalHeading').text('Create Tour Package')
  $('.editSubDivisionBtn').addClass('d-none')
  $('.addSubDivisionBtn').text('Create')
  $('.addSubDivisionBtn').data('id', null)
  beatsList = []

  $('#beatPointsTable tbody').html('')
  resetForm(formEle)
  addPointRow()

  $(formEle+' .inputNameLabel').addClass('active')
                          
  $('#addTourPackageModal').modal('open')
}

function addPointRow() {

  $('#itineraryTable tbody').append(`<tr data-id="0">
                                        <td class="text-center">1</td>

                                        <td class="text-center">
                                          <div class="defaultLocation d-flex">
                                            <input type="text" class="form-control itrldate" placeholder="Select Date">
                                          </div>
                                        </td>

                                        <td class="text-center">
                                        <div class="defaultLocation d-flex">
                                        <textarea id="activities" name="activ" class="materialize-textarea itrldesc" placeholder="Enter itenararydesc" maxlength="1000"></textarea>
                                        </div>
                                        </td>

                                        <td class="text-center">
                                          <div class="defaultLocation d-flex">
                                            <input type="text" class="form-control  itrlocation" placeholder="Enter Location">
                                          </div>
                                        </td>

                                        <td class="text-center hideOnViewOnly">
                                          <span class="table-remove">
                                            <button type="button" class="btn-danger btn-rounded btn-sm my-0"><i class="fa-minus fas"></i></button>
                                          </span>
                                          <span class="table-add d-none">
                                            <button type="button" class="btn-success btn-rounded btn-sm my-0"><i class="fa-plus fas"></i></button>
                                          </span>
                                        </td>

                                      </tr>`);



    $('.itrldate').bsdatepicker({
      format: dateformat_type.DisplayDate_Small,
      autoclose: true
      }).on('changeDate', function (e) {
      $(this).parent().find('.datePicker i').removeClass('fa-calendar-alt').addClass('fa-calendar-times');
    });

  updatePointsIndex()

}


// function readImageURL(input) {
//   if (input.files && input.files[0]) {
//     var reader = new FileReader();

//     reader.onload = function (e) {
//       $('.eventExistingImg').attr("href", e.target.result)
//       $('.eventExistingImgDiv').removeClass('d-none')
//     }

//     reader.readAsDataURL(input.files[0]);
//   } else {
//     $('.eventExistingImg').attr('href', '')
//     $('.eventExistingImgDiv').addClass('d-none')
//   }
// }

function readImageURL(input) {
  if (input.files && input.files[0]) {
    const file = input.files[0];
    const validImageTypes = ['image/jpeg', 'image/png', 'image/gif'];
    if (!validImageTypes.includes(file.type)) {
      input.value = ''; 
      $('#psSchedulefilename').val(''); 
      $('.eventExistingImgDiv').addClass('d-none'); 
      return;
    }

    const reader = new FileReader();
    reader.onload = function (e) {

      $('.eventExistingImgDiv img.eventExistingImg').attr('src', e.target.result);
      $('.eventExistingImgDiv a.eventExistingImg').attr('href', e.target.result);
      $('.eventExistingImgDiv').removeClass('d-none'); 
    };
    reader.readAsDataURL(file);
  } else {
    $('.eventExistingImgDiv img.eventExistingImg').attr('src', '/static/images/fileIcons/image_icon.jpg');
    $('.eventExistingImgDiv a.eventExistingImg').attr('href', '');
    $('.eventExistingImgDiv').addClass('d-none');
  }
}

function removeImgFile(ele) {
  $('.eventExistingImg').attr('href', '')
  $('#psSchedulefile').val('')
  $('#psSchedulefilename').val('')
  $('.eventExistingImgDiv').addClass('d-none')
}

function updatePointsIndex() {

  $('#itineraryTable tbody tr').each(function (index) {
    $(this).find('td:first-child').text(index + 1)
    $(this).find('.table-remove').removeClass('d-none')
    $(this).find('.table-add').addClass('d-none')
  });

  if($('#itineraryTable tbody tr').length > 1)
    $('#itineraryTable tbody tr:last .table-remove').removeClass('d-none')
  else
    $('#itineraryTable tbody tr:last .table-remove').addClass('d-none')
  $('#itineraryTable tbody tr:last .table-add').removeClass('d-none')
}

//remove button click event
$(document).on("click", ".table-remove", function () {

  $(this).parents('tr').remove();
  updatePointsIndex()
})

$(document).on("click", ".table-add", function () {

  if (validateForm('#itineraryTable tbody')) {

    addPointRow();
  }
})

function typeChangeAction(ele) {

  var arr = $.grep(beatsList, function( obj, index ) {
    return ( obj.id == ele.value );
  });
  
  var poiPoints = []
  if(arr.length > 0) {
    poiPoints = arr[0].poiPoints;
  }

  var html = '<option value="">Select BeatPoint</option>';
  $.each(poiPoints, function (index, obj) {
    html += '<option value="' + obj.id + '">' + obj.title + '</option>';
  });
  $(ele).closest('tr').find('.beatPoints').html(html)

}

function beatPointChangeAction(ele) {
  
  $(this).find('td:first-child').text();

  $('#beatPointsTable tbody tr').each(function (index) {
    if($(this).find('td:first-child').text() != $(ele).closest('tr').find('td:first-child').text() && $(this).find('.beatPoints').val() == ele.value) {
      $(ele).val('')
      show_StatusModal('Beat Point already added', statusEnum.error)
    }
  });
}

function subDivisionSelected(ele) {

  var arr = $.grep(subDivsWisePSList, function( obj, index ) {
    return ( obj.id == ele.value );
  });
  
  var circles = []
  if(arr.length > 0) {
    circles = arr[0].circles;
  }

  setDropdownsWith({data: circles, placeholder: 'Select Circle'}, function (optionsHtml) {
    $('#routeCircle').html(optionsHtml)
    $('#routeCircle').formSelect();
  })
  setDropdownsWith({data: [], placeholder: 'Select Police Station'}, function (optionsHtml) {
    $('#routePoliceStation').html(optionsHtml)
    $('#routePoliceStation').formSelect();
  })

}

function circleSelected(ele) {

  var subDivisionId = $('#routeSubDivision').val();

  var arr = $.grep(subDivsWisePSList, function( obj, index ) {
    return ( obj.id == subDivisionId );
  });

  if(arr.length == 0) return;

  arr = $.grep(arr[0].circles, function( obj, index ) {
    return ( obj.id == ele.value );
  });
  
  var policeStations = []
  if(arr.length > 0) {
    policeStations = arr[0].policeStations;
  }

  setDropdownsWith({data: policeStations, placeholder: 'Select Police Station'}, function (optionsHtml) {
    $('#routePoliceStation').html(optionsHtml)
    $('#routePoliceStation').formSelect();
  })
}

function psSelected(ele) {

  if(isInvalidString(ele.value)) {
    return
  }

  getPSUsers(ele.value, function () {})
  getPOIs(ele.value, function () {})
}

function getPSUsers(policeStationId, completionCallback) {

  $.ajax({
    url: baseUrl + 'policeStations/users?policeStationId=' + policeStationId,
    type: "GET",
    contentType: "application/json",
    dataType: 'json',
    success: function (result) {
      if (apiResStatus(result.status)) {
        
        setDropdownsWith({data: result.data, placeholder: 'Select Incharge'}, function (optionsHtml) {
          $('#routeIncharge').html(optionsHtml)
          $('#routeIncharge').formSelect();
        })

        completionCallback();
      } else {
        $('#routeIncharge').html(`<option value="">Select Incharge</option>`)
        completionCallback();
        show_StatusModal(result.message, result.status)
      }
    },
    error: function (data, textStatus, jqXHR) {
      errorHandledCallBack(data, textStatus, jqXHR, function () {
        $('#routeIncharge').html(`<option value="">Select Incharge</option>`)
        completionCallback();
      })
    }
  });

}

function getPOIs(policeStationId, completionCallback) {

  var payload = {
    "keyword": "",
    "classification": "",
    "category": [],
    "type": [],
    "source": "",
    "createdUser": null,
    "flatten": 'TYPES'
  }

  $.ajax({
    url: baseUrl + 'poiCategories/poi?policeStationId=' + policeStationId,
    type: "POST",
    contentType: "application/json",
    dataType: 'json',
    data: JSON.stringify(payload),
    success: function (result) {
      if (apiResStatus(result.status)) {
        
        beatsList = result.data;
        setDropdownsWith({data: result.data, placeholder: 'Select Type'}, function (optionsHtml) {
          $('.poiType').html(optionsHtml)
          $('.poiType').val('')
        })
        setDropdownsWith({data: [], placeholder: 'Select BeatPoint'}, function (optionsHtml) {
          $('.beatPoints').html(optionsHtml)
          $('.beatPoints').val('')
        })

        completionCallback();
      } else {
        beatsList = [];
        completionCallback();
        show_StatusModal(result.message, result.status)
      }
    },
    error: function (data, textStatus, jqXHR) {
      errorHandledCallBack(data, textStatus, jqXHR, function () {
        beatsList = [];
        completionCallback();
      })
    }
  });

}

function addTourPackageAction() {
  var formEle = '#stdRouteForm'
  if( $('.addSubDivisionBtn').text() == 'Edit') {
    removeViewMode(formEle)
    $('.addTourPackageBtn').text('Update')
    $('.tourPackageModalHeading').text('Edit Standard Route')
    $('.editTourPackageBtn').addClass('d-none')

  } else if (validateForm(formEle)) {

    var stdRouteForm = document.getElementById("tourPackageForm");
    var formData = new FormData(stdRouteForm);

    var fileInput = document.getElementById("psSchedulefile");
    if (fileInput.files.length > 0) {
      formData.append("image", fileInput.files[0]);
    }

    // Check if an image is previewed
    formData.append('existingImg', $('.eventExistingImgDiv img.eventExistingImg').attr('src') == '/static/images/fileIcons/image_icon.jpg' ? '' : 'containImg');

    
    var start_date = convertDateFormater($("#pstateDate").val(),dateformat_type.DayMonthYear, dateformat_type.ServerDate)
    var end_date = convertDateFormater($("#pendDate").val(),dateformat_type.DayMonthYear, dateformat_type.ServerDate)

    formData.append('start_date', start_date);
    formData.append('end_date', end_date);
    
    var Itinerary = []

    $('#itineraryTable tbody tr').each(function (index) {
      var desc = $(this).find('.itrldesc').val()
      var loc = $(this).find('.itrlocation').val()
      var date = $(this).find('.itrldate').val()
      var obj = {
        desc: desc,
        loc: loc,
        date:convertDateFormater(date,dateformat_type.DayMonthYear, dateformat_type.ServerDate)
      }
      Itinerary.push(obj)
    });

    formData.append('Itinerary', JSON.stringify(Itinerary));

    var type = 'POST'
    var id = $('.addTourPackageBtn').data('id')
    if(id != null) {
      formData.append('id', id);
      type = 'PUT'
    }
    $.ajax({
      url: baseUrl + 'tour/add_tour_package',
      data: formData,
      cache: false,
      processData: false,
      contentType: false,
      type: type,
      success: function (result) {
        if (apiResStatus(result.status)) {
          $('#table_content').DataTable().draw()
          $('#addTourPackageModal').modal('close')
          show_StatusModal(result.message, result.status)
        } else {
          show_StatusModal(result.message, result.status)
        }
      },
      error: errorCallBack
    });
  }

}

function centerEditAction(ele, forView = false) {

  var id = $(ele).closest('tr').data('id')
  var arr = $.grep(packageData.data, function( obj ) {
    return obj.torp_id == id;
  });

  if(arr.length > 0) {
    setSubDivisionDetails(arr[0], forView)
    $('#addTourPackageModal').modal('open')
  }

}

function setSubDivisionDetails(data, forView) {

  $('.tourPackageModalHeading').text(forView ? 'Package' : 'Edit Package')
  $('.addTourPackageBtn').text(forView ? 'Edit' : 'Update')
  forView ? $('.editTourPackageBtn').removeClass('d-none') : $('.editTourPackageBtn').addClass('d-none')
  $('.addTourPackageBtn').data('id', data.sbtr_id)

  $('#itineraryTable tbody').html('')

  var formEle = '#tourPackageForm'
  resetForm(formEle)

  setTimeout(function(){ 
    
    $(formEle + ' input[name=name]').val(data.torp_name)
    $(formEle + ' select[name=packagetype]').val(data.torp_package_type).formSelect().change()
    $(formEle + ' input[name=price]').val(data.torp_price)
    $(formEle + ' input[name=duration]').val(data.torp_duration)
    $(formEle + ' input[name=startdate]').val(data.torp_start_date)
    $(formEle + ' input[name=enddate]').val(data.torp_end_date)
    $(formEle + ' select[name=pdestination]').val(data.torp_destination).formSelect()
    $(formEle + ' select[name=pstatelocation]').val(data.torp_start_location).formSelect()
    $(formEle + ' select[name=pstatelocation]').val(data.torp_end_destination).formSelect()
    $(formEle + ' textarea[name=description]').val(data.torp_description)
    $(formEle + ' textarea[name=inclusion]').val(data.torp_inclusions)

    M.textareaAutoResize($(formEle + ' textarea[name=description]'));
    M.textareaAutoResize($(formEle + ' textarea[name=inclusion]'));
    
    if (isInvalidString(data.torp_image)) {
      $(formEle + ' .eventExistingImgDiv img.eventExistingImg').attr('src', '/static/images/fileIcons/image_icon.jpg');
      $(formEle + ' .eventExistingImgDiv').addClass('d-none');
    } else {
      $(formEle + ' .eventExistingImgDiv img.eventExistingImg').attr('src', serverEndPointUrl+'/'+data.torp_image);
      $(formEle + ' .eventExistingImgDiv').removeClass('d-none');
    }

    // if (isInvalidString(data.torp_image)) {
    //   $(formEle + ' .Categorylogoimg').attr('src', '')
    //   $('.existingImgDiv').addClass('d-none')
    // } else {
    //     $(formEle + ' .Categorylogoimg').attr('src', data.torp_image)
    //     $('.existingImgDiv').removeClass('d-none')
    // }
      $.each(data.itinerary, function (index, obj) {
        addPointRow()
        $('#itineraryTable tbody tr:last .itrldate').val(obj.itnr_date)
        $('#itineraryTable tbody tr:last .itrldesc').val(obj.itnr_activities)
        $('#itineraryTable tbody tr:last .itrlocation').val(obj.itnr_location)
      });
   
    $(formEle + ' .inputNameLabel').addClass('active')

    checkViewMode(formEle, forView)
    
  }, 500);

}

function centerDeleteAction(ele) {

  conformationDialog('Confirmation', 'Are you sure to delete.', 'Cancel', 'Delete', function (conformation) {
    if (!conformation) return;
	
    var payload = {
      id: $(ele).closest('tr').data('id')
    }

    $.ajax({
      url: baseUrl + 'stdBeatRoutes',
      type: "DELETE",
      contentType: "application/json",
      dataType: 'json',
      data: JSON.stringify(payload),
      success: function (result) {
        if (apiResStatus(result.status)) {
          $('#table_content').DataTable().draw()
          show_StatusModal(result.message, result.status)
        } else {
          show_StatusModal(result.message, result.status)
        }
      },
      error: errorCallBack
    });

  })
}

function updateStatusAction(id, status) {

  var payload = {
    id: id,
    status: status
  }

  $.ajax({
    url: baseUrl + 'tour/change_status',
    type: "PATCH",
    contentType: "application/json",
    dataType: 'json',
    data: JSON.stringify(payload),
    success: function (result) {
      if (apiResStatus(result.status)) {
        $('#table_content').DataTable().draw()
        show_StatusModal(result.message, result.status)
      } else {
        show_StatusModal(result.message, result.status)
      }
    },
    error: errorCallBack
  });

}