import axios from 'axios'

const state = {
    companyid: '',
    datas: []
}

const getters = {
    dantis:state=>{
		return state.datas;
    }
}

const  mutations = {
    setCompanyid(state, data){
        state.companyid = data
    },
    setDantis(state, data){
        state.datas = data
    },
    removeDanti(state,data){
        var index = state.datas.indexOf(data)
        state.datas.splice(index,1)
    }
}

const actions = {
    getDantis(context){
        axios.get(`/kong/gongdi_mng/v1.0/company/${context.state.companyid}/dantis`)
		.then(function(response){
            context.commit('setDantis',response.data)
            console.log("actions",response);
		}).catch(function(error){
			console.log("actions");
		})
    },
    postDantis(context,data){
        console.log(data)        
        axios.post('/kong/gongdi_mng/v1.0/dantis',data)
		.then(response => {
            if (response.status === 201) {
                data = state.datas 
                data.unshift(response.data)
                context.commit('setDantis', data)
                // alert('新增成功！')
            }
            else {
                alert('新增失败')
            }
		}).catch(function(error){
			alert('请求失败')
		})
    },
    putDantis(context,data){
        delete data.comp_name
        delete data.dantiid
        axios.put(`/kong/gongdi_mng/v1.0/dantis/${data.id}`,data)
        .then(response => {
            if(response.status === 201){
                var i = 0, len = state.datas.length
                for(;i<len;i++){
                    if(state.datas[i].id === data.id){
                        var newDatas = state.datas
                        console.log(newDatas)
                        newDatas[i] = response.data 
                        console.log(newDatas)                        
                        context.commit('setDantis',newDatas)
                        break
                    }
                }
            }
        })
        .catch(error => {
            alert('出错')
        })
    },
    removeDantis(context,data){
        axios.delete(`http://127.0.0.1:8889/gongdi_mng/v1.0/dantis/${data.id}`)
			.then(function(response){
                if(response.status === 204){
                    context.commit('removeDanti',data)
                }
			}).catch(function(error){
			})
    }
}

export default {
    state,
    getters,
    mutations,
    actions
}