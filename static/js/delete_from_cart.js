function delete_from_cart(del){

    var item_id = $(del).data('item_id');
    var url = '/delete_from_cart/';
    var csrf_token = $('#dummy_form [name="csrfmiddlewaretoken"]').val();
    console.log(csrf_token);
      var data = {};
        data.item_id = item_id;
        data['csrfmiddlewaretoken'] = csrf_token;
        console.log(data);
        $.ajax({
            url:url,
            type:'POST',
            data: data,
            cache:true,
            success: function (data) {
                console.log('OK');
                console.log(data.all_items);
                $('.cart_table_lg').empty();
                if (data.all_items.length > 0) {
                     $.each(data.all_items,function (k,v) {
                    $('.cart_table_lg').append('     \t<tr>\n' +
                        '\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class="product-thumbnail">\n' +
                        '\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<a href="page-detail.html">\n' +
                        '\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<img width="80" height="107" alt="" class="img-responsive" src="'+ v.image +'">\n' +
                        '\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</a>\n' +
                        '\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</td>\n' +
                        '\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class="product-name">\n' +
                        '\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<a href="page-detail.html">'+ v.name +'</a>\n' +
                        '\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<br><span class="amount"><strong>'+ v.number+' X '+ v.price +' &#8381; = '+ v.total_price +' &#8381;</strong></span>\n' +
                        '\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</td>\n' +
                        '\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<td class="product-actions">\n' +
                        '\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<a data-item_id="'+ v.id +'" class="remove" onclick="delete_from_cart(this);return false;"> <i class="fa fa-times"></i> </a></td>\n' +
                        '\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<i class="fa fa-times"></i>\n' +
                        '\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</a>\n' +
                        '\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</td>\n' +
                        '\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</tr>');


                });
                $('.cart_total_lg').html(data.total_cart_price);
                $('.cart_footer_lg').html('');
                $('.cart_footer_lg').append('' +
                    ' <h3 class="text-right subtotal"> ИТОГО: '+ data.total_cart_price +' &#8381; </h3>\n' +
                    '                            <a class="btn  btn-danger" href="/cart"> <i class="fa fa-shopping-cart"> </i> ПРОСМОТР КОРЗИНЫ</a><a\n' +
                    '                                class="btn  btn-primary"> ОПЛАТА</a>');
                }
                else
                {
                    $('.cart_total_lg').html('0');
                    $('.cart_footer_lg').html('');
                    $('.cart_footer_lg').append('<h3 class="text-right subtotal"> КОРЗИНА ПУСТА </h3>');
                    $('#checkout_btn').attr('disabled','disabled');
                }
            },
            error: function () {
                console.log('ERROR')
            }
        });
console.log($(del).data('item_id'));
 // $(del).closest('li').remove();
}
