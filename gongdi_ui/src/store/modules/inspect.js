import axios from 'axios'

const state = {
    buweis:[],
}

const getters = {
    buweis:state=>{
        return state.buweis
    }
}

const  mutations = {
    setBuweis(state, data){
        state.buweis = data
    },
    removeBuweis(state,data){
        var index = state.buweis.indexOf(data)
        state.buweis.splice(index,1)
    },
}

const actions = {
    getBuweis(context,data){
        axios.get(`/kong/gongdi_mng/v1.0/dantis/${data}/buweis`)
        .then(response=>{
            if(response.status === 200){
                context.commit('setBuweis',response.data)
            }
        })
    },
    postBuwei(context,data){
        axios.post('/kong/gongdi_mng/v1.0/buweis',data)
		.then(response => {
            if (response.status === 201) {
                data = context.getters.buweis 
                data.unshift(response.data)
                context.commit('setBuweis', data)
            }
            else {
                alert('新增失败')
            }
		}).catch(function(error){
			alert('请求失败')
		})
    },
    putBuweis(context,data){
        console.table(data)
        delete data.danti_name
        delete data.dantiid
        axios.put(`/kong/gongdi_mng/v1.0/buweis/${data.id}`,data)
        .then(response => {
            if(response.status === 201){
                for(var item of context.getters.buweis){
                    if(item.id === data.id){
                        var index = context.getters.buweis.indexOf(item)
                        var [...newDatas] = context.getters.buweis
                        newDatas.splice(index, 1, response.data)
                        context.commit('setBuweis',newDatas)
                        break
                    }
                }
            }
        })
        .catch(error => {
            alert('出错')
        })
    },
    removeBuweis(context,data){
        axios.delete(`/kong/gongdi_mng/v1.0/buweis/${data.id}`)
			.then(function(response){
                if(response.status === 204){
                    context.commit('removeBuweis',data)
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