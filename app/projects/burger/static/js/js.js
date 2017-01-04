$(function(){
	$('.single-item').slick({
		  slidesToShow: 3,
		  autoplay:true,
		  autoplaySpeed:1000,
		  dots:true,
		  arrows: false,
		  speed:1000,
		  focusOnSelect:true
	});

	$('.cafe-block').slick({
		  slidesToShow: 1,
		  autoplay:true,
		  autoplaySpeed:2000,
		  dots:false,
		  arrows: false,
		  focusOnSelect:false
	});

	require.config({
            paths: {
                echarts: 'static/js/echarts-2.2.7/build/dist'
            }
        });
        require(
            [
                'echarts',
                'echarts/chart/pie'
            ],
            function (ec) {
                var myChart = ec.init(document.getElementById('main')); 
                
                var option = {
                tooltip : {
                    trigger: 'item',
                    formatter: "{a} <br/>{b} : {c} ({d}%)"
                },
                legend: {
                    orient : 'vertical',
                    x : 'left',
                    data:['ALABAMA','ATLANTA','JACKDANIELS','BIG DADDY','KANZAS','CALIFORNIA','UNCLESAM','PAPASHEEPSMINI']
                },
                toolbox: {
                    show : true,
                    feature : {
                        mark : {show: false},
                        dataView : {show: false, readOnly: false},
                        magicType : {
                            show: false, 
                            type: ['pie', 'funnel'],
                            option: {
                                funnel: {
                                    x: '25%',
                                    width: '50%',
                                    funnelAlign: 'left',
                                    max: 1548
                                }
                            }
                        },

                        restore : {show: true,
                                    title:"reload"},
                        saveAsImage : {show: true,
                                        title:"save"}
                    },
                    borderColor:'#000000'
                },
                calculable : true,
                color:['#FCBD5A', '#A24C25','#7C2903', '#C81504', '#F1301E','#F1691E','#F77A08','#F79D08' ],
                backgroundColor:"#FDCA6D",
                series : [
                    {
                        name:'имя',
                        type:'pie',
                        radius : '80%',
                        center: ['50%', '50%'],
                        data:[
                            {value:3145, name:'ALABAMA'},
                            {value:2809, name:'ATLANTA'},
                            {value:4533, name:'JACKDANIELS'},
                            {value:7566, name:'BIG DADDY'},
                            {value:1050, name:'KANZAS'},
                            {value:3789, name:'CALIFORNIA'},
                            {value:3871, name:'UNCLESAM'},
                            {value:2537, name:'PAPASHEEPSMINI'},
                        ]
                                                    
                    }
                ]
            };
                myChart.setOption(option); 
            }
        );
});
