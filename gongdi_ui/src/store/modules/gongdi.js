import axios from 'axios'

const state = {
    companyid: '',
    datas: [],
}

const getters = {
    gongdis:state=>{
		return state.datas;
    }
}

const  mutations = {
    setCompanyid(state, data){
        state.companyid = data
    },
    setGongdis(state, data){
        state.datas = [data]
    },
    removeGongdi(state,data){
        var index = state.datas.indexOf(data)
        state.datas.splice(index,1)
    },
    setCompanies(state,data){
        state.companies = data
    }
}

const actions = {
    getCompanies(context){
        axios.get('/kong/employeemng/v1.0/companys')
        .then(response=>{
            if(response.status === 200){
                context.commit('setCompanies',response.data)
            }
        })
    },
    getGongdis(context){
        axios.get(`/kong/gongdi_mng/v1.0/companys/${context.state.companyid}/gongdis`)
		.then(response => {
            context.commit('setGongdis',response.data)
            console.log("actions",response);
		}).catch(function(error){
			console.log("actions");
		})
    },
    postGongdis(context,data){
        axios.post('/kong/gongdi_mng/v1.0/gongdis',data)
		.then(response => {
            if (response.status === 201) {
                data = state.datas 
                data.unshift(response.data)
                context.commit('setGongdis', data)
            }
            else {
                alert('新增失败')
            }
		}).catch(function(error){
			alert('请求失败')
		})
    },
    putGongdis(context,data){
        delete data.comp_name
        delete data.gongdiid
        axios.put(`/kong/gongdi_mng/v1.0/gongdis/${data.id}`,data)
        .then(response => {
            if(response.status === 201){
                var i = 0, len = context.getters.gongdis.length
                for(;i<len;i++){
                    if(context.getters.gongdis[i].id === data.id){
                        var newDatas = context.getters.gongdis
                        newDatas[i] = response.data 
                        context.commit('setGongdis',newDatas)
                        // console.log(context.getters.gongdis)
                        break
                    }
                }
            }
        })
        .catch(error => {
            alert('出错')
        })
    },
    removeGongdis(context,data){
        axios.delete(`http://127.0.0.1:8889/gongdi_mng/v1.0/gongdis/${data.id}`)
			.then(function(response){
                if(response.status === 204){
                    context.commit('removeGongdi',data)
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