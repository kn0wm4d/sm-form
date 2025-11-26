import {
  createApp,
  nextTick,
} from "https://unpkg.com/petite-vue?module";
// import { transitionDirective } from "https://unpkg.com/vue-petite-transition?module";

function FieldComponent(props) {
  return {
    $template: "#field-component-template",
    field: props.field,
    fieldNum: props.currentStep + props.index + 1,

    get isInvalid() {
      return props.isInvalid();
    },
    get invalidMessage() {
      return props.invalidMessage();
    },
    get nextStep() {
      nextTick(() => {
        this.$refs.InputFields?.focus();
        // this.focusElem(this.$refs.InputFields);
        //this.$refs.InputFields.setAttribute("autofocus", "true");
        // this.invalids = {};
      });
    },
    // methods
    validate() {
      nextTick(() => {
        if (this.isInvalid) {
          props.validate();
        }
      });
    },
  };
}

function StepsIndicatorComponent(props) {
  return {
    $template: "#step-indicator-component-template",
    stepsCount: props.stepsCount,
    get stepsCountWithSuccessPage() {
      return this.stepsCount + 1;
    },
  };
}

createApp({
  // Components
  StepsIndicatorComponent,
  FieldComponent,

  // Data
  formstarted: false,
  currentStep: 0,
  submitted: false,
  submitSuccess: false,
  submitError: false,
  formAccessKey: "YOUR_ACCESS_KEY_HERE",
  invalids: {},
  fields: {
    email: {
      label: "Email",
      value: "",
      validations: [
        {
          message: "Must be a valid email address",
          test: (value) => validateEmail(value),
        },
        {
          message: "Email is required",
          test: (value) => value,
        },
      ],
    },
    name: {
      label: "Name",
      value: "",
      validations: [
        {
          message: "Name is a required field",
          test: (value) => value,
        },
      ],
    },
    gender: {
      label: "Gender / النوع",
      value: "",
      type: "select",
      name: "gender",
      options: [
        "Male / ذكر",
        "Female / أنثى",
      ],
      validations: [
        {
          message: "Gender is a required field",
          test: (value) => value,
        },
      ],
    },
    age: {
      label: "Age / العمر",
      value: "",
      type: "select",
      name: "age",
      options: [
        "18-25",
        "25-30",
        "30+",
      ],
      validations: [
        {
          message: "Age is a required field",
          test: (value) => value,
        },
      ],
    },
    phone: {
      label: "Phone Number / رقم الهاتف",
      value: "",
      validations: [
        {
          message: "Phone Number is a required field",
          test: (value) => value,
        },
      ],
    },
    whatsapp: {
      label: "WhatsApp Number / رقم الواتساب",
      value: "",
      validations: [
        {
          message: "WhatsApp Number is a required field",
          test: (value) => value,
        },
      ],
    },
    residency: {
      label: "Residency / مكان الإقامة",
      value: "",
      type: "select",
      name: "residency",
      options: [
        "Mokattam / المقطم",
        "Maadi / المعادي",
        "Nasr City / مدينة نصر",
        "Tagamo (1st / 3rd / 5th) / التجمع (الأول / الثالث / الخامس)",
        "Misr al-Jadida / مصر الجديدة",
        "Faisal / فيصل",
        "Dokki / الدقي",
        "Mohandiseen / المهندسين",
        "Hadayek El Ahram / حدائق الأهرام",
        "6th October / السادس من أكتوبر",
        "Helwan / حلوان",
        "Madinaty / مدينتي",
        "Shorooq / الشروق",
        "Obour / العبور",
        "Rehab / الرحاب",
        "Badr City / بدر",
        "Shubra / شبرا",
      ],
      validations: [
        {
          message: "Residency is a required field",
          test: (value) => value,
        },
      ],
    },
    career: {
      label: "Where are you currently in your career? / أين أنت حاليا في حياتك المهنية؟",
      value: "",
      type: "select",
      name: "career",
      options: [
        "Student / طالب",
        "Fresh Graduate / خريج حديثا",
        "Career Shifting / تغيير مسار مهني",
      ],
      validations: [
        {
          message: "Career status is a required field",
          test: (value) => value,
        },
      ],
    },
    workshops1: {
      label: "What workshops do you want to attend? (10 AM – 12 PM)",
      value: [],
      type: "multiselect",
      name: "workshops1",
      options: [
        "كيف تستعد لـ OET",
        "Medical Research and Scientific Writing",
        "مهارات الجراح الموهوب",
        "Clinical Skills",
      ],
      optional: true,
      validations: [],
    },
    workshops2: {
      label: "What workshops do you want to attend? (12 PM – 2 PM)",
      value: [],
      type: "multiselect",
      name: "workshops2",
      options: [
        "ICDL",
        "الإسعافات الأولية",
        "اتخرجت يا دكتور وبعدين؟",
        "أسرار السيرة الذاتية",
      ],
      optional: true,
      validations: [],
    },
    workshops3: {
      label: "What workshops do you want to attend? (2 PM – 4 PM)",
      value: [],
      type: "multiselect",
      name: "workshops3",
      options: [
        "الإلقاء والصوت",
        "كتابة المحتوى",
        "How to Live a Healthy Lifestyle",
        "بتعرف شنو عن ريادة الأعمال؟",
      ],
      optional: true,
      validations: [],
    },
    workshops4: {
      label: "What workshops do you want to attend? (4 PM – 6 PM)",
      value: [],
      type: "multiselect",
      name: "workshops4",
      options: [
        "مهارات البيع الاحترافي",
        "Communication Skills",
        "Freelance",
        "Graphic Design",
      ],
      optional: true,
      validations: [],
    },
    workshops5: {
      label: "What workshops do you want to attend? (6 PM – 8 PM)",
      value: [],
      type: "multiselect",
      name: "workshops5",
      options: [
        "كيف تبقى صانع محتوى",
        "Digital Marketing",
        "افكارك مرآة افعالك",
        "التحدث امام الجمهور",
      ],
      optional: true,
      validations: [],
    },
  },
  steps: [
    ["email"],
    ["name"],
    ["gender"],
    ["age"],
    ["phone"],
    ["whatsapp"],
    ["residency"],
    ["career"],
    ["workshops1"],
    ["workshops2"],
    ["workshops3"],
    ["workshops4"],
    ["workshops5"],
  ],

  // Getters
  get currentFields() {
    return this.steps[this.currentStep];
  },
  get totalSteps() {
    return this.steps.length;
  },
  get isFirstStep() {
    return this.currentStep === 0;
  },
  get isLastStep() {
    return this.currentStep === this.totalSteps - 1;
  },

  startForm() {
    return (this.formstarted = true);
  },

  // Methods
  previousStep() {
    if (this.isFirstStep) return;
    // removes all invalids so doesn't show error messages on back
    this.invalids = {};
    this.currentStep--;
  },
  nextStep() {
    if (this.isLastStep) return;
    this.validate();
    //console.log(this);
    if (this.isInvalid) return;
    this.currentStep++;
  },
  get isInvalid() {
    return !!Object.values(this.invalids).filter((key) => key).length;
  },

  // methods
  validate() {
    this.invalids = {};
    // validates all the fields on the current page
    this.currentFields.forEach((key) => {
      this.validateField(key);
    });
  },
  validateField(fieldKey) {
    this.invalids[fieldKey] = false;
    const field = this.fields[fieldKey];
    // run through each of the fields validation tests
    field.validations.forEach((validation) => {
      if (!validation.test(field.value)) {
        this.invalids[fieldKey] = validation.message;
      }
    });
  },
  listenEnterKey() {
    window.addEventListener("keydown", (e) => {
      if (e.key == "Enter") {
        e.preventDefault();
        if (!this.formstarted) {
          this.formstarted = true;
        } else if (!this.isLastStep && !this.isInvalid) {
          return this.nextStep();
        } else {
          return this.submit();
        }
      }
    });
  },
  async submit() {
    // if form not valid don't submit
    this.validate();
    if (this.isInvalid) return;
    this.submitted = true;
    const formData = this.fields;
    const object = {
      access_key: this.formAccessKey,
      subject: "New submission from multistep form",
    };
    for (const key in formData) {
      object[key] = formData[key].value;
    }
    console.log("Submitting form..", object);

    const response = await fetch("https://api.web3forms.com/submit", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify(object),
    });
    const result = await response.json();

    if (result.success) {
      console.log(result);
      // submit on valid form
      this.submitSuccess = true;
    } else {
      console.log(result);
      this.submitError = true;
    }

    // this will also work.
    // for (let [key, value] of Object.entries(formData)) {
    //   console.log(key, value.value);
    // }
  },
})
  // .directive("transition", transitionDirective)
  .mount("#multistep-form");

function validateEmail(email) {
  const re =
    /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(String(email).toLowerCase());
}
