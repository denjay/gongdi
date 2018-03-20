import axios from 'axios'

const state = {
    gongdis: [],
}

const getters = {
    gongdis:state=>{
		return state.gongdis;
    }
}

const  mutations = {
    setGongdis(state, data){
        state.gongdis = data
    },
    removeGongdi(state,data){
        var index = state.gongdis.indexOf(data)
        state.gongdis.splice(index,1)
    },
}

const actions = {
    getGongdis(context,data){
        axios.get(`/kong/gongdi_mng/v1.0/companys/${data}/gongdis`)
		.then(response => {
            if(response.data.length === 0){
                context.commit('setGongdis',[])
            }
            else {
                context.commit('setGongdis',[response.data])
            }
		}).catch(function(error){
			console.log("actions");
		})
    },
    postGongdis(context,data){
        axios.post('/kong/gongdi_mng/v1.0/gongdis',data)
		.then(response => {
            if (response.status === 201) {
                data = context.getters.gongdis
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
        if (data.starttime === null){
            data.starttime = ""
        }
        if (data.complete_time === null){
            data.complete_time = ""
        }
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
    },
    removeGongdis(context,data){
        axios.delete(`/kong/gongdi_mng/v1.0/gongdis/${data.id}`)
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