<template>
  <div>
    <div class="">
      <el-collapse v-model="activeNames">
        <el-collapse-item title="可选筛选项" name="1">
          <div class="select">
            <span>选择部位：</span>
            <el-select v-model="filterData.companyid" filterable clearable placeholder="请选择公司">
              <el-option
                v-for="company in companies"
                :key="company.id"
                :label="company.company_name"
                :value="company.id">
              </el-option>
            </el-select>
            <el-select v-model="filterData.dantiid" filterable clearable placeholder="请选择单体">
              <el-option
                v-for="danti in dantis"
                :key="danti.id"
                :label="danti.name"
                :value="danti.id">
              </el-option>
            </el-select>
            <el-select v-model="filterData.buweiid" filterable clearable placeholder="请选择部位">
              <el-option
                v-for="buwei in buweis"
                :key="buwei.id"
                :label="buwei.name"
                :value="buwei.id">
              </el-option>
            </el-select>
            <br>            
            <span>施工单位：</span>
            <el-input
              placeholder="请输入施工单位"
              v-model="filterData.shigong_danwei"
              clearable>
            </el-input>
            <br>            
            <span>交底人：</span>
            <el-input
              placeholder="请输入交底人"
              v-model="filterData.jiaodi_ren"
              clearable>
            </el-input>
            <br>            
            <span>被交底人：</span>
            <el-input
              placeholder="请输入被交底人"
              v-model="filterData.bei_jiaodi_ren"
              clearable>
            </el-input>
          </div>
        </el-collapse-item>
      </el-collapse>
      <el-button @click="getJiaodis(1)" type="primary">查询</el-button>
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
        width="100">
      </el-table-column>
      <el-table-column
        prop="name"
        width="150"
        label="交底名">
      </el-table-column>
      <el-table-column
        prop="buwei_name"
        width="150"
        label="所属部位">
      </el-table-column>
      <el-table-column
        prop="jiaodi_time"
        label="交底时间"
        width="100"
        :formatter="formatter">
      </el-table-column>
      <el-table-column
        prop="shigong_danwei"
        width="200"
        label="施工单位">
      </el-table-column>
      <el-table-column
        prop="jiaodi_ren"
        width="100"
        label="交底人">
      </el-table-column>
      <el-table-column
        prop="bei_jiaodi_ren"
        width="100"
        label="被交底人">
      </el-table-column>
      <el-table-column
        prop="description"
        label="描述">
      </el-table-column>
      <el-table-column
        fixed="right"
        label="操作"
        width="180">
        <template slot-scope="scope">
          <el-button @click="remove(scope.row)" size="mini" icon="el-icon-delete"></el-button>
          <el-button @click="edit(scope.row)" size="mini" icon="el-icon-edit"></el-button>
          <el-button @click="file_manage(scope.row)" size="mini" icon="el-icon-document"></el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      v-show="Number(total_datas)"
      background
      layout="prev, pager, next"
      :current-page.sync="cur_page"
      @current-change="handleCurrentChange"
      :page-size="page_size"
      :page-count="total_pages">
    </el-pagination>

    <el-dialog title="文档附件管理" :visible.sync="dialogVisible_file" width="60%" :before-close="handleClose">
      <el-table
        :data="doc_files"
        border
        style="width: 100%">
        <el-table-column
          fixed
          prop="id"
          label="id"
          width="100">
        </el-table-column>
        <el-table-column
          prop="file_size"
          width="150"
          label="文件大小(kb)">
        </el-table-column>
        <el-table-column
          prop="file_name"
          label="文件名">
        </el-table-column>
        <el-table-column
          fixed="right"
          label="操作"
          width="130">
          <template slot-scope="scope">
            <el-button @click="remove(scope.row)" size="mini" icon="el-icon-delete"></el-button>
            <a :href="`/kong/gongdi_mng/v1.0/doc_files/${scope.row.id}`">
              <el-button size="mini" icon="el-icon-download"></el-button>
            </a>
          </template>
        </el-table-column>
      </el-table>

      <el-upload
        class="upload-demo"
        ref="upload"
        action="/kong/gongdi_mng/v1.0/doc_files"
        multiple
        name="doc"
        :data={docsid:docsid}
        :before-remove="beforeRemove"
        :on-change="handleChange"            
        :auto-upload="false"
        :file-list="fileList">
        <el-button size="small" type="primary">选择文件</el-button>
      </el-upload>
    </el-dialog>
    
    <el-dialog
      :title="title"
      :visible.sync="dialogVisible_doc"
      width="30%"
      :before-close="handleClose">
      <el-form label-position="right" label-width="100px" :model="formData" :rules="rules" ref="ruleForm">
        <template v-if="title === '新增交底'">
          <el-form-item label="公司名称" prop="companyid">
            <el-select v-model="formData.companyid" filterable clearable placeholder="请选择公司">
              <el-option
                v-for="company in companies"
                :key="company.id"
                :label="company.company_name"
                :value="company.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="所属单体" prop="dantiid">
            <el-select v-model="formData.dantiid" filterable clearable placeholder="请选择单体">
              <el-option
                v-for="danti in dantis"
                :key="danti.id"
                :label="danti.name"
                :value="danti.id">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="所属部位" prop="buweiid">
            <el-select v-model="formData.buweiid" filterable clearable placeholder="请选择部位">
              <el-option
                v-for="buwei in buweis"
                :key="buwei.id"
                :label="buwei.name"
                :value="buwei.id">
              </el-option>
            </el-select>
          </el-form-item>
        </template>
        <el-form-item label="编号" prop="code">
          <el-input
            placeholder="请输入文档编号"
            v-model="formData.code"
            clearable>
          </el-input>
        </el-form-item>        
        <el-form-item label="交底名称" prop="name">
          <el-input
            placeholder="请输入交底名称"
            v-model="formData.name"
            clearable>
          </el-input>
        </el-form-item>
        <el-form-item label="交底时间" prop="jiaodi_time">
          <el-date-picker v-model="formData.jiaodi_time" type="date" placeholder="选择日期"></el-date-picker>          
        </el-form-item>
        <el-form-item label="施工单位" prop="shigong_danwei">
          <el-input
            placeholder="请输入施工单位"
            v-model="formData.shigong_danwei"
            clearable>
          </el-input>
        </el-form-item>
        <el-form-item label="交底人" prop="jiaodi_ren">
          <el-input
            placeholder="请输入交底人"
            v-model="formData.jiaodi_ren"
            clearable>
          </el-input>
        </el-form-item>
        <el-form-item label="被交底人" prop="bei_jiaodi_ren">
          <el-input
            placeholder="请输入被交底人"
            v-model="formData.bei_jiaodi_ren"
            clearable>
          </el-input>
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            type="textarea"
            :rows="2"
            placeholder="请输入内容"
            v-model="formData.description">
          </el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="resetForm('ruleForm')">取 消</el-button>
        <el-button type="primary" @click="submitForm('ruleForm')">确 定</el-button>
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
        docsid : null,
        fileList:[],        
        rules: {
          companyid: [
            { required: true, message: '请选择所属公司', trigger: 'change' },
          ],
          dantiid: [
            { required: true, message: '请选择所属单体', trigger: 'change' },
          ],
          buweiid: [
            { required: true, message: '请选择所属部位', trigger: 'change' },
          ],
          code: [
            { required: true, message: '请输入文件编码', trigger: 'blur' },
          ],
          name: [
            { required: true, message: '请输入文档名', trigger: 'blur' },
          ],
          shigong_danwei: [
            { required: true, message: '请输施工单位', trigger: 'blur' },
          ],
          jiaodi_ren: [
            { required: true, message: '请输入交底人', trigger: 'blur' },
          ],
          bei_jiaodi_ren: [
            { required: true, message: '请输入被交底人', trigger: 'blur' },
          ]
        },
        filterData:{
          companyid: '',
          dantiid: '',
          buweiid: null,
          shigong_danwei: '',
          jiaodi_ren: '',
          bei_jiaodi_ren: '',
        },
        formData:{
          companyid: '',
          dantiid: '',
          buweiid: null,
          code: null,
          name: null, 
          jiaodi_time: '',
          shigong_danwei: '',
          jiaodi_ren: '',
          bei_jiaodi_ren: '',
          description: ''
        },
        page_size: 15,
        cur_page:1,
        jiaodi_id: null,
        activeNames: ['1'],
        dialogVisible_doc: false,
        dialogVisible_file: false,
        title: '',
      }
    },

    methods: {
      handleCurrentChange(val) {
        this.getJiaodis(val)
      },
      // 用于格式化时间显示的值
      formatter(row, column) {
        if(Boolean(row.jiaodi_time)){
          var date = new Date(row.jiaodi_time)
          return date.toLocaleDateString();
        }
      },
      getJiaodis(page){
        this.$store.dispatch('jiaodi/getJiaodis', {
          "page":page,
          "per_page":this.page_size,
          "buwei":this.buwei_name,
          "shigong_unit":this.filterData.shigong_danwei,
          "jiaodi_ren":this.filterData.jiaodi_ren,
          "bei_jiaodi_ren":this.filterData.bei_jiaodi_ren
          })        
      },
      insert(){
        // 新增时先清空表单数据        
        this.title = '新增交底'
        this.dialogVisible_doc = true
        this.formData.jiaodi_time = ''
        this.formData.shigong_danwei = ''
        this.formData.jiaodi_ren = ''
        this.formData.bei_jiaodi_ren = ''
        this.formData.name = ''
        this.formData.code = ''
        this.formData.description = ''
      },
      edit(data){
        // 点编辑时，将对应行数据写入表单   
        this.title = '编辑交底'
        this.jiaodi_id = data.id
        this.formData.name = data.name
        this.formData.code = data.code
        this.formData.jiaodi_time = data.jiaodi_time
        this.formData.shigong_danwei = data.shigong_danwei
        this.formData.jiaodi_ren = data.jiaodi_ren
        this.formData.bei_jiaodi_ren = data.bei_jiaodi_ren
        this.formData.description = data.description
        this.dialogVisible_doc = true
      },
      resetForm(formName) {
        this.$refs[formName].resetFields();
        this.dialogVisible_doc = false
      },
      submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            this.submitData();
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
      submitData(){
        // 组织表单需要的数据，创建或更新数据        
        var data = {
          code:this.formData.code,
          name:this.formData.name,
          buweiid:this.formData.buweiid,
          jiaodi_time:this.formData.jiaodi_time,
          shigong_danwei:this.formData.shigong_danwei,
          jiaodi_ren:this.formData.jiaodi_ren,
          bei_jiaodi_ren:this.formData.bei_jiaodi_ren,
          description:this.formData.description,
        }
        if(!Boolean(data.jiaodi_time)){
          delete data.jiaodi_time
        }
        else{
          // 解决时间格式不对的问题
          data.jiaodi_time = new Date(data.jiaodi_time)
        }
        if(this.title === '新增交底'){
          this.$store.dispatch('jiaodi/postJiaodis',data)
        }
        else if(this.title === '编辑交底'){
          data["id"] = this.jiaodi_id
          delete data.buweiid          
          this.$store.dispatch('jiaodi/putJiaodis',data)
        }
        this.dialogVisible_doc = false
      },
      remove(data) {
        this.$confirm('此操作將永久刪除該資料, 是否繼續?', '提示', {
          confirmButtonText: '確定',
          cancelButtonText: '取消',
        }).then(() => {
          // 删除一条数据之后的页数
          var total_pages =  Math.ceil((this.total_datas-1) / this.page_size)
          this.$store.dispatch('jiaodi/removeJiaodis',data);
          // 解决删除一条数据后，当前页大于总页数的问题
          var page = this.cur_page > total_pages ? total_pages : this.cur_page;
          this.getJiaodis(page)
        })
      },
      file_manage(data){
        this.$store.dispatch('jiaodi/doc_files/getDocFiles', data.id)  
        this.docsid = data.id
        this.dialogVisible_file = true      
      },
      handleClose(done) {
        this.$confirm('确认关闭？')
          .then(_ => {
            done();
          })
      },
      // upload相关
      beforeRemove(file, fileList) {
        return this.$confirm(`确定移除 ${ file.name }？`);
      },
      handleChange(file, fileList) {
        this.fileList = fileList;
      } 
    },

    computed: {
      total_pages(){
        return Math.ceil(this.total_datas / this.page_size)
      },
      buwei_name(){
        if(Boolean(this.filterData.buweiid)){
          return this.buweis.filter(item => item.id === this.filterData.buweiid)[0]["name"]
        }
      },
      ...mapGetters('jiaodi/buwei',{
        'dantis':'dantis',
        'companies':'companies',
        'buweis':'buweis',
        }
      ),
      ...mapGetters('jiaodi/doc_files',{
        'doc_files':'doc_files',
        }
      ),
      ...mapGetters('jiaodi',{
        'jiaodis':'jiaodis',
        'total_datas':'total_datas',
		  }),
    },

    watch:{
      "filterData.companyid": function(){
        this.filterData.dantiid = ''
        this.$store.commit('jiaodi/buwei/setDantis',[])
        if(Boolean(this.filterData.companyid)){
          this.$store.dispatch('jiaodi/buwei/getDantis', {companyid:this.filterData.companyid})
        }
      },
      "filterData.dantiid": function(){
        this.filterData.buweiid = null
        this.$store.commit('jiaodi/buwei/setBuweis',[])
        if(Boolean(this.filterData.dantiid)){
          this.$store.dispatch('jiaodi/buwei/getBuweis', this.filterData.dantiid)
        }
      },
      "formData.companyid": function(){
        this.formData.dantiid = ''
        this.$store.commit('jiaodi/buwei/setDantis',[])
        if(Boolean(this.formData.companyid)){
          this.$store.dispatch('jiaodi/buwei/getDantis', {companyid:this.formData.companyid})
        }
      },
      "formData.dantiid": function(){
        this.formData.buweiid = null
        this.$store.commit('jiaodi/buwei/setBuweis',[])
        if(Boolean(this.formData.dantiid)){
          this.$store.dispatch('jiaodi/buwei/getBuweis', this.formData.dantiid)
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
  .select .el-select {
    width: 200px;
    margin-bottom: 20px;
  } 
  .select {
    width: 700px;
    margin-right: 20px;
    display: inline-block;
  }
  .select .el-input {
    margin-bottom: 20px;
  }
  .el-input {
    width: 200px;
  }
  .el-textarea {
    width: 200px;
  }
</style>

<style>
  /* .el-dialog {
    width: 385px !important;
  } */
  .el-table {
    margin-top: 5px;
  }
  .el-collapse-item__header {
    width: 120px;
    font-size: 16px;
    color: #409eff;
  }
</style>
