<template>
  <div>
    <div class="">
      <el-collapse v-model="activeNames">
        <el-collapse-item title="可选筛选项" name="1">
          <div class="select">
            <span>请选择部位：</span>
            <el-select v-model="companyid" filterable clearable placeholder="请选择公司">
              <el-option
                v-for="company in companies"
                :key="company.id"
                :label="company.company_name"
                :value="company.id">
              </el-option>
            </el-select>
            <el-select v-model="dantiid" filterable clearable placeholder="请选择单体">
              <el-option
                v-for="danti in dantis"
                :key="danti.id"
                :label="danti.name"
                :value="danti.id">
              </el-option>
            </el-select>
            <el-select v-model="buweiid" filterable clearable placeholder="请选择部位">
              <el-option
                v-for="buwei in buweis"
                :key="buwei.id"
                :label="buwei.name"
                :value="buwei.id">
              </el-option>
            </el-select>
            <br>
            <span>请选择日期：</span>
            <el-date-picker v-model="insp_date" value-format="yyyy-MM-dd" type="date" placeholder="选择日期"></el-date-picker>
            <br>
            <span>巡检人姓名：</span>
            <el-input
              placeholder="请输入巡检人姓名"
              v-model="insp_emp"
              clearable>
            </el-input>
          </div>
        </el-collapse-item>
      </el-collapse>
      <el-button @click="getInspects" type="primary">查询</el-button>
      <el-button @click="insert" type="primary" :disabled="!(companyid && dantiid && buweiid)">新增巡检</el-button>
    </div>

    <el-collapse v-model="activeNames">
      <el-collapse-item title="质量巡检" name="2">
        <el-table
          :data="quality_inspects"
          border
          style="width: 100%">
          <el-table-column
            fixed
            prop="insp_date"
            label="巡检日期"
            width="150">
          </el-table-column>
          <el-table-column
            prop="insp_emp"
            label="巡检人">
            width="200"
          </el-table-column>
          <el-table-column
            prop="buwei_name"
            label="部位名称">
            width="200"
          </el-table-column>
          <el-table-column
            prop="description"
            label="描述">
          </el-table-column>
          <el-table-column
            prop="is_qualified"
            label="是否合格">
          </el-table-column>
          <el-table-column
            fixed="right"
            label="操作"
            width="100">
            <template slot-scope="scope">
              <el-button @click="remove(scope.row)" type="text" size="mini" icon="el-icon-delete"></el-button>
              <el-button @click="edit(scope.row)" type="text" size="mini" icon="el-icon-edit"></el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-collapse-item>
      <el-collapse-item title="安全巡检" name="3">
        <el-table
          :data="safety_inspects"
          border
          style="width: 100%">
          <el-table-column
            fixed
            prop="insp_date"
            label="巡检日期"
            width="150">
          </el-table-column>
          <el-table-column
            prop="insp_emp"
            label="巡检人">
            width="200"
          </el-table-column>
          <el-table-column
            prop="buwei_name"
            label="部位名称">
            width="200"
          </el-table-column>
          <el-table-column
            prop="description"
            label="描述">
          </el-table-column>
          <el-table-column
            prop="is_qualified"
            label="是否合格">
          </el-table-column>
          <el-table-column
            fixed="right"
            label="操作"
            width="100">
            <template slot-scope="scope">
              <el-button @click="remove(scope.row)" type="text" size="mini" icon="el-icon-delete"></el-button>
              <el-button @click="edit(scope.row)" type="text" size="mini" icon="el-icon-edit"></el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-collapse-item>
      <el-collapse-item title="产品巡检" name="4">
        <el-table
          :data="produce_inspects"
          border
          style="width: 100%">
          <el-table-column
            fixed
            prop="insp_date"
            label="巡检日期"
            width="150">
          </el-table-column>
          <el-table-column
            prop="insp_emp"
            label="巡检人">
            width="200"
          </el-table-column>
          <el-table-column
            prop="buwei_name"
            label="部位名称">
            width="200"
          </el-table-column>
          <el-table-column
            prop="description"
            label="描述">
          </el-table-column>
          <el-table-column
            prop="is_qualified"
            label="是否合格">
          </el-table-column>
          <el-table-column
            fixed="right"
            label="操作"
            width="100">
            <template slot-scope="scope">
              <el-button @click="remove(scope.row)" type="text" size="mini" icon="el-icon-delete"></el-button>
              <el-button @click="edit(scope.row)" type="text" size="mini" icon="el-icon-edit"></el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-collapse-item>
    </el-collapse>

    <el-dialog
      :title="title"
      :visible.sync="dialogVisible"
      width="30%"
      :before-close="handleClose">

      <el-form label-position="right" label-width="100px" :model="insertData">
        <el-form-item label="部位名称">
          <el-input v-model="insertData.name"></el-input>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="insertData.description"></el-input>
        </el-form-item>
      </el-form>

      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitData">确 定</el-button>
      </span>
    </el-dialog>

  </div>
</template>

<script>
  import {mapGetters} from 'vuex'
  export default {
    mounted(){
      this.$store.dispatch('getCompanies')
    },

    data() {
      return {
        companyid: '',
        dantiid: '',
        buweiid: null,
        insp_date: null,
        insp_emp: null, 
        insp_type: null,
        insp_types: ["quality_inspects", "safety_inspects", "produce_inspects"],
        activeNames: ['1'],
        dialogVisible: false,
        title: '',
        insertData:{
          name: '',
          description: ''
        }
      }
    },

    methods: {
      getInspects(){
          this.$store.dispatch('getInspects', 
          { "buweiid":this.buweiid, "insp_date":this.insp_date, "insp_emp":this.insp_emp })        
      },
      insert(){
        this.title = '新增部位'
        this.dialogVisible = true
      },
      edit(data){
        this.title = '编辑部位'
        var { ...data_copy } = data
        this.insertData = data_copy
        this.dialogVisible = true
      },
      submitData(){
        var {...insertData} = this.insertData
        if(this.title === '新增部位'){
          insertData['dantiid'] = parseInt(this.dantiid)
          this.$store.dispatch('postBuwei',insertData)
        }
        else if(this.title === '编辑部位'){
          this.$store.dispatch('putBuweis',insertData)
        }
        // 重置form
        this.dialogVisible = false
        this.insertData = {
          name: '',
          description: ''
        }
      },
      remove(data) {
        this.$confirm('此操作將永久刪除該資料, 是否繼續?', '提示', {
          confirmButtonText: '確定',
          cancelButtonText: '取消',
        }).then(() => {
          this.$store.dispatch('removeBuweis',data);
        }).catch(() => {         
        });
      },
      handleClose(done) {
        this.$confirm('确认关闭？')
          .then(_ => {
            done();
          })
          .catch(_ => {});
      }
    },

    computed: {
      ...mapGetters([
        'dantis',
        'companies',
        'buweis',
        'quality_inspects',
        'safety_inspects',
        'produce_inspects',
		  ])
    },

    watch:{
      companyid: function(){
        this.dantiid = ''
        this.$store.commit('setDantis',[])
        debugger
        if(Boolean(this.companyid)){
          this.$store.dispatch('getDantis', this.companyid)
        }
      },
      dantiid: function(){
        this.buweiid = ''
        this.$store.commit('setBuweis',[])
        if(Boolean(this.dantiid)){
          this.$store.dispatch('getBuweis', this.dantiid)
        }
      },
    }     
  }
</script>

<style scoped>
  .el-select {
    width: 200px;
    margin-bottom: 20px;
  }
  .el-dialog {
    width: 350px !important;
  }
  .select {
    width: 700px;
    margin-right: 20px;
    display: inline-block;
  }
  .el-input {
    width: 200px;
    margin-bottom: 20px;
  }
</style>

<style>
  .el-table {
    margin-top: 5px;
  }
  .el-collapse-item__header {
    width: 120px;
    font-size: 16px;
    color: #409eff;
  }
</style>
