<template>
  <div>
    <div class="">
      <el-collapse v-model="activeNames">
        <el-collapse-item title="可选筛选项" name="1">
          <div class="select">
            <span>选择部位：</span>
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
            <!-- <br>
            <span>文档名：</span>
            <el-input
              placeholder="请输入文档名"
              v-model="name"
              clearable>
            </el-input> -->
            <br>            
            <span>施工单位：</span>
            <el-input
              placeholder="请输入施工单位"
              v-model="shigong_danwei"
              clearable>
            </el-input>
            <br>            
            <span>交底人：</span>
            <el-input
              placeholder="请输入交底人"
              v-model="jiaodi_ren"
              clearable>
            </el-input>
            <br>            
            <span>被交底人：</span>
            <el-input
              placeholder="请输入被交底人"
              v-model="bei_jiaodi_ren"
              clearable>
            </el-input>
          </div>
        </el-collapse-item>
      </el-collapse>
      <el-button @click="getJiaodis" type="primary">查询</el-button>
      <el-button @click="insert" type="primary">新增交底</el-button>
    </div>

    <el-table
      :data="jiaodis"
      border
      style="width: 100%">
      <el-table-column
        fixed
        prop="code"
        label="编号"
        width="150">
      </el-table-column>
      <el-table-column
        prop="name"
        width="200"
        label="交底名">
      </el-table-column>
      <el-table-column
        prop="buwei_name"
        width="200"
        label="所属部位">
      </el-table-column>
      <el-table-column
        prop="jiaodi_time"
        label="交底时间"
        width="200"
        :formatter="formatter">
      </el-table-column>
      <el-table-column
        prop="shigong_danwei"
        width="200"
        label="施工单位">
      </el-table-column>
      <el-table-column
        prop="jiaodi_ren"
        width="200"
        label="交底人">
      </el-table-column>
      <el-table-column
        prop="bei_jiaodi_ren"
        width="200"
        label="被交底人">
      </el-table-column>
      <el-table-column
        prop="description"
        label="描述">
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

    <el-dialog
      :title="title"
      :visible.sync="dialogVisible"
      width="30%"
      :before-close="handleClose">
      <el-form label-position="right" label-width="100px">
        <template v-if="title === '新增交底'">
          <el-form-item label="公司名称">
            <el-select v-model="companyid" filterable clearable placeholder="请选择公司">
              <el-option
                v-for="company in companies"
                :key="company.id"
                :label="company.company_name"
                :value="company.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="所属单体">
            <el-select v-model="dantiid" filterable clearable placeholder="请选择单体">
              <el-option
                v-for="danti in dantis"
                :key="danti.id"
                :label="danti.name"
                :value="danti.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="所属部位">
            <el-select v-model="buweiid" filterable clearable placeholder="请选择部位">
              <el-option
                v-for="buwei in buweis"
                :key="buwei.id"
                :label="buwei.name"
                :value="buwei.id">
              </el-option>
            </el-select>
          </el-form-item>
        </template>
        <el-form-item label="编号">
          <el-input
            placeholder="请输入文档编号"
            v-model="code"
            clearable>
          </el-input>
        </el-form-item>
        <el-form-item label="交底时间">
          <el-date-picker v-model="jiaodi_time" type="date" placeholder="选择日期"></el-date-picker>          
        </el-form-item>
        <!-- <el-form-item label="文档名称">
          <el-input
            placeholder="请输入文档名称"
            v-model="name"
            clearable>
          </el-input>
        </el-form-item> -->
        <el-form-item label="施工单位">
          <el-input
            placeholder="请输入施工单位"
            v-model="shigong_danwei"
            clearable>
          </el-input>
        </el-form-item>
        <el-form-item label="交底人">
          <el-input
            placeholder="请输入交底人"
            v-model="jiaodi_ren"
            clearable>
          </el-input>
        </el-form-item>
        <el-form-item label="被交底人">
          <el-input
            placeholder="请输入被交底人"
            v-model="bei_jiaodi_ren"
            clearable>
          </el-input>
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            type="textarea"
            :rows="2"
            placeholder="请输入内容"
            v-model="description">
          </el-input>
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
      this.$store.dispatch('jiaodi/buwei/getCompanies')
    },

    data() {
      return {
        companyid: '',
        dantiid: '',
        buweiid: null,
        jiaodi_id: null,
        // name: null, 
        code: null,
        description: '',
        shigong_danwei: '',
        jiaodi_ren: '',
        bei_jiaodi_ren: '',
        jiaodi_time: '',
        activeNames: ['1'],
        dialogVisible: false,
        title: '',
      }
    },

    methods: {
      // 用于格式化时间显示的值
      formatter(row, column) {
        var date = new Date(row.jiaodi_time)
        return date.toLocaleDateString();
      },
      getJiaodis(){
        this.$store.dispatch('jiaodi/getJiaodis', {
          "buwei":this.buwei_name,
          // "doc_name":this.name,
          "shigong_unit":this.shigong_danwei,
          "jiaodi_ren":this.jiaodi_ren,
          "bei_jiaodi_ren":this.bei_jiaodi_ren
          })        
      },
      insert(){
        this.title = '新增交底'
        this.dialogVisible = true
        this.name = ''
        this.code = ''
        this.description = ''
      },
      edit(data){
        this.title = '编辑交底'
        this.jiaodi_id = data.id
        this.name = data.name
        this.code = data.code
        this.description = data.description
        this.dialogVisible = true
      },
      submitData(){
        var data = {
          code:this.code,
          name:this.name,
          buweiid:this.buweiid,
          description:this.description,
        }
        if(this.title === '新增交底'){
          this.$store.dispatch('jiaodi/postJiaodis',data)
        }
        else if(this.title === '编辑交底'){
          data["id"] = this.jiaodi_id
          delete data.buweiid          
          this.$store.dispatch('jiaodi/putJiaodis',data)
        }
        this.dialogVisible = false
      },
      remove(data) {
        this.$confirm('此操作將永久刪除該資料, 是否繼續?', '提示', {
          confirmButtonText: '確定',
          cancelButtonText: '取消',
        }).then(() => {
          this.$store.dispatch('jiaodi/removeJiaodis',data);
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
      buwei_name(){
        if(Boolean(this.buweiid)){
          return this.buweis.filter(item => item.id === this.buweiid)[0]["name"]
        }
      },
      ...mapGetters('jiaodi/buwei',{
        'dantis':'dantis',
        'companies':'companies',
        'buweis':'buweis',
        }
      ),
      ...mapGetters('jiaodi',{
        'jiaodis':'jiaodis',
		  }),
    },

    watch:{
      companyid: function(){
        this.dantiid = ''
        this.$store.commit('jiaodi/buwei/setDantis',[])
        if(Boolean(this.companyid)){
          this.$store.dispatch('jiaodi/buwei/getDantis', this.companyid)
        }
      },
      dantiid: function(){
        this.buweiid = null
        this.$store.commit('jiaodi/buwei/setBuweis',[])
        if(Boolean(this.dantiid)){
          this.$store.dispatch('jiaodi/buwei/getBuweis', this.dantiid)
        }
      },
    }     
  }
</script>

<style scoped>
  .select span {
    display:inline-block;
    width: 70px;
  }
  .el-select {
    width: 200px;
    margin-bottom: 20px;
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
  .el-form-item {
    margin-bottom: 0px;
  }
  .el-textarea {
    width: 200px;
  }
</style>

<style>
  .el-dialog {
    width: 385px !important;
  }
  .el-table {
    margin-top: 5px;
  }
  .el-collapse-item__header {
    width: 120px;
    font-size: 16px;
    color: #409eff;
  }
</style>
