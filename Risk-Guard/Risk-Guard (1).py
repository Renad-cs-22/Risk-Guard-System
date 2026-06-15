#!/usr/bin/env python
# coding: utf-8

# In[1]:


import hashlib
import json
from datetime import datetime

class RiskGuardSystem:
    def __init__(self):
        self.pending_requests = {} # العمليات المعلقة في انتظار التحقق
        self.audit_log = []        # سجل التدقيق الأمني
        self.last_log_hash = "0"   # بصمة السجل السابق (مفهوم شبيه بسلسلة الكتل لضمان عدم التلاعب)

    def create_transaction(self, maker_name, amount, description):
        """يقوم الصانع (Maker) بإنشاء طلب عملية جديدة"""
        tx_id = f"TXN-{int(datetime.now().timestamp())}"
        
        # تقييم مخاطر تلقائي بناءً على المبلغ
        risk_level = "High (عالي)" if amount > 50000 else "Medium (متوسط)"
        
        transaction = {
            "Transaction_ID": tx_id,
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Maker": maker_name,
            "Amount": amount,
            "Description": description,
            "Risk_Level": risk_level,
            "Status": "Pending Approval (في انتظار الاعتماد)"
        }
        
        self.pending_requests[tx_id] = transaction
        print(f"\n[+] [Maker] قام الموظف ({maker_name}) بإنشاء عملية برقم: {tx_id}")
        print(f"    ⚠️ تقييم المخاطر التلقائي للعملية: {risk_level}")
        return tx_id

    def verify_transaction(self, tx_id, checker_name, action):
        """يقوم المتحقق (Checker) بمراجعة العملية (اعتماد أو رفض)"""
        if tx_id not in self.pending_requests:
            print("❌ خطأ: رقم العملية غير موجود أو تم معالجته مسبقاً!")
            return

        tx = self.pending_requests[tx_id]

        # حماية أمنية: منع الصانع من أن يكون هو نفسه المتحقق لضمان الفصل بين الواجبات
        if tx["Maker"] == checker_name:
            print(f"🚨 [إنتهاك أمني] لا يمكن للموظف ({checker_name}) اعتماد عملية قام بإنشائها بنفسه!")
            return

        if action.lower() in ['اعتماد', 'approve', 'y']:
            tx["Status"] = "Approved & Executed"
            print(f"✅ [Checker] قام المشرف ({checker_name}) باعتماد وتنفيذ العملية {tx_id} بنجاح.")
        else:
            tx["Status"] = "Rejected"
            print(f"❌ [Checker] قام المشرف ({checker_name}) برفض العملية {tx_id}.")

        tx["Checker"] = checker_name
        tx["Verification_Time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # نقل العملية إلى سجل التدقيق المشفر وتطهير قائمة المعلقات
        self._add_to_immutable_audit_log(tx)
        del self.pending_requests[tx_id]

    def _add_to_immutable_audit_log(self, transaction):
        """إضافة العملية إلى سجل تدقيق مشفر بربط كل سجل بالذي قبله (Chain of Logs)"""
        tx_string = json.dumps(transaction, sort_keys=True)
        
        # دمج بيانات العملية الحالية مع بصمة السجل السابق لمنع تعديل السجلات القديمة
        combined_data = tx_string + self.last_log_hash
        current_hash = hashlib.sha256(combined_data.encode()).hexdigest()
        
        audit_entry = {
            "Data": transaction,
            "Previous_Hash": self.last_log_hash,
            "Current_Hash": current_hash
        }
        
        self.audit_log.append(audit_entry)
        self.last_log_hash = current_hash # تحديث البصمة المرجعية للسجل القادم

    def display_audit_trail(self):
        """عرض سجل التدقيق كاملاً لغايات الـ Compliance والرقابة"""
        print("\n" + "="*30 + " 📊 سجل التدقيق الأمني (Audit Trail) " + "="*30)
        for entry in self.audit_log:
            print(f"ID: {entry['Data']['Transaction_ID']} | الحالة: {entry['Data']['Status']}")
            print(f"الصانع (Maker): {entry['Data']['Maker']} | المتحقق (Checker): {entry['Data'].get('Checker', 'N/A')}")
            print(f"المبلغ: {entry['Data']['Amount']} | المخاطر: {entry['Data']['Risk_Level']}")
            print(f"🔗 الـ Hash الحالي للسجل: {entry['Current_Hash']}")
            print("-" * 80)

if __name__ == "__main__":
    print(" 🛡️ RiskGuard: Maker-Checker & Immutable Audit System 🛡️ ")
    system = RiskGuardSystem()

    # سيناريو تجريبي يحاكي العمل الحقيقي
    # 1. إنشاء عمليات بواسطة Maker
    tx1 = system.create_transaction(maker_name="أحمد", amount=75000, description="شراء خوادم جديدة للموقع")
    tx2 = system.create_transaction(maker_name="سارة", amount=12000, description="تجديد تراخيص البرمجيات")

    # 2. محاولة اختراق الضوابط (أحمد يحاول اعتماد عمليته بنفسه)
    print("\n--- محاولة فحص اختراق الضوابط الأمنية ---")
    system.verify_transaction(tx_id=tx1, checker_name="أحمد", action="اعتماد")

    # 3. الاعتماد الصحيح والمنفصل للواجبات
    print("\n--- معالجة العمليات بشكل صحيح ---")
    system.verify_transaction(tx_id=tx1, checker_name="ريناد", action="اعتماد") # ريناد تدقق على أحمد
    system.verify_transaction(tx_id=tx2, checker_name="أحمد", action="اعتماد")  # أحمد يدقق على سارة

    # 4. طباعة السجل النهائي للامتثال
    system.display_audit_trail()


# In[1]:


import hashlib
import json
import uuid
from datetime import datetime

class RiskGuardSystem:
    def __init__(self):
        # استخدام القواميس لضمان سرعة الوصول والتحقق
        self.pending_requests = {} 
        self.audit_log = []        
        self.last_log_hash = "0"   

    def create_transaction(self, maker_name: str, amount: float, description: str) -> str:
        """ينشئ طلب عملية جديد بمعرف فريد كلياً وتقييم آلي للمخاطر."""
        if amount <= 0:
            raise ValueError("❌ خطأ: يجب أن يكون مبلغ العملية أكبر من صفر!")

        # حل مشكلة تكرار المعرفات باستخدام UUID4
        unique_id = uuid.uuid4().hex[:8].upper()
        tx_id = f"TXN-{datetime.now().strftime('%Y%m%d')}-{unique_id}"
        
        # تقييم المخاطر (تم تحسين الشرط ليكون أكثر مرونة)
        risk_level = "High (عالي)" if amount > 50000 else "Medium (متوسط)"
        
        transaction = {
            "Transaction_ID": tx_id,
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Maker": maker_name.strip(),
            "Amount": amount,
            "Description": description.strip(),
            "Risk_Level": risk_level,
            "Status": "Pending Approval"
        }
        
        self.pending_requests[tx_id] = transaction
        print(f"\n[+] [Maker] الموظف ({maker_name}) أنشأ عملية برقم: {tx_id}")
        print(f"    ⚠️ تقييم المخاطر التلقائي: {risk_level}")
        return tx_id

    def verify_transaction(self, tx_id: str, checker_name: str, action: str) -> bool:
        """يراجع العملية ويمنع الصانع من الاعتماد تحقيقاً لمبدأ الفصل بين الواجبات (SoD)."""
        tx = self.pending_requests.get(tx_id)
        
        if not tx:
            print(f"❌ خطأ: رقم العملية {tx_id} غير موجود أو تمت معالجته مسبقاً!")
            return False

        # حماية أمنية صارمة: الفصل بين الواجبات (Segregation of Duties)
        if tx["Maker"].lower() == checker_name.strip().lower():
            print(f"🚨 [انتهاك أمني] لا يمكن للموظف ({checker_name}) اعتماد عملية قام بإنشائها بنفسه!")
            return False

        # توحيد التحقق من حالة القرار
        is_approved = action.strip().lower() in ['اعتماد', 'approve', 'y', 'yes']
        
        tx["Status"] = "Approved & Executed" if is_approved else "Rejected"
        tx["Checker"] = checker_name.strip()
        tx["Verification_Time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # ترحيل السجل وتطهير القائمة المعلقة
        self._add_to_immutable_audit_log(tx)
        del self.pending_requests[tx_id]
        
        status_emoji = "✅" if is_approved else "❌"
        status_text = "باعتماد" if is_approved else "برفض"
        print(f"{status_emoji} [Checker] المشرف ({checker_name}) قام {status_text} العملية {tx_id} .")
        return True

    def _add_to_immutable_audit_log(self, transaction: dict):
        """يربط السجل الحالي بالسجل السابق عبر تشفير SHA-256 لمنع التلاعب (Blockchain Concept)."""
        # استخدام ensure_ascii=False للحفاظ على النصوص العربية داخل الـ JSON وبثبات الترتيب
        tx_string = json.dumps(transaction, sort_keys=True, ensure_ascii=False)
        
        # بناء الكتلة المشفرة
        combined_data = f"{tx_string}{self.last_log_hash}"
        current_hash = hashlib.sha256(combined_data.encode('utf-8')).hexdigest()
        
        audit_entry = {
            "Data": transaction,
            "Previous_Hash": self.last_log_hash,
            "Current_Hash": current_hash
        }
        
        self.audit_log.append(audit_entry)
        self.last_log_hash = current_hash 

    def display_audit_trail(self):
        """يعرض سجل التدقيق الأمني لغايات الامتثال الرقابي وضمان سلامة البيانات."""
        print("\n" + "="*25 + " 📊 سجل التدقيق الأمني (Audit Trail) " + "="*25)
        for entry in self.audit_log:
            data = entry['Data']
            print(f"ID: {data['Transaction_ID']} | الحالة: {data['Status']}")
            print(f"الصانع: {data['Maker']} | المدقق: {data.get('Checker', 'N/A')}")
            print(f"المبلغ: {data['Amount']} | المخاطر: {data['Risk_Level']}")
            print(f"🔗 الـ Hash الحالي : {entry['Current_Hash']}")
            print(f"⛓️ الـ Hash السابق: {entry['Previous_Hash']}")
            print("-" * 86)

if __name__ == "__main__":
    print(" 🛡️ RiskGuard: Maker-Checker & Immutable Audit System 🛡️ ")
    system = RiskGuardSystem()

    # 1. إنشاء عمليات
    tx1 = system.create_transaction(maker_name="أحمد", amount=75000, description="شراء خوادم جديدة")
    tx2 = system.create_transaction(maker_name="سارة", amount=12000, description="تجديد تراخيص")

    # 2. فحص محاولة اختراق السياسات الأمنية
    print("\n--- محاولة فحص اختراق الضوابط الأمنية ---")
    system.verify_transaction(tx_id=tx1, checker_name="أحمد", action="اعتماد")

    # 3. معالجة صحيحة (الفصل بين الواجبات)
    print("\n--- معالجة العمليات بشكل صحيح ---")
    system.verify_transaction(tx_id=tx1, checker_name="ريناد", action="approve") 
    system.verify_transaction(tx_id=tx2, checker_name="أحمد", action="اعتماد")  

    # 4. عرض سجل الامتثال
    system.display_audit_trail()


# In[ ]:


import hashlib
import json
import uuid
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

class RiskGuardSystem:
    def __init__(self):
        self.pending_requests = {} 
        self.audit_log = []        
        self.last_log_hash = "0"   

    def create_transaction(self, maker_name: str, amount: float, description: str) -> str:
        if amount <= 0:
            raise ValueError("المبلغ يجب أن يكون أكبر من صفر")
        unique_id = uuid.uuid4().hex[:8].upper()
        tx_id = f"TXN-{datetime.now().strftime('%Y%m%d')}-{unique_id}"
        risk_level = "High (عالي)" if amount > 50000 else "Medium (متوسط)"
        
        transaction = {
            "Transaction_ID": tx_id,
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Maker": maker_name.strip(),
            "Amount": amount,
            "Description": description.strip(),
            "Risk_Level": risk_level,
            "Status": "Pending Approval"
        }
        self.pending_requests[tx_id] = transaction
        return tx_id

    def verify_transaction(self, tx_id: str, checker_name: str, action: str) -> tuple:
        tx = self.pending_requests.get(tx_id)
        if not tx:
            return False, "العملية غير موجودة أو عولجت مسبقاً"
        if tx["Maker"].lower() == checker_name.strip().lower():
            return False, f"🚨 انتهاك أمني: لا يمكن للمنشئ ({checker_name}) اعتماد عمليته!"
        
        is_approved = action.lower() in ['اعتماد', 'approve', 'y', 'yes']
        tx["Status"] = "Approved & Executed" if is_approved else "Rejected"
        tx["Checker"] = checker_name.strip()
        tx["Verification_Time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self._add_to_immutable_audit_log(tx)
        del self.pending_requests[tx_id]
        return True, f"تمت معالجة العملية بنجاح بحالة: {tx['Status']}"

    def _add_to_immutable_audit_log(self, transaction: dict):
        tx_string = json.dumps(transaction, sort_keys=True, ensure_ascii=False)
        combined_data = f"{tx_string}{self.last_log_hash}"
        current_hash = hashlib.sha256(combined_data.encode('utf-8')).hexdigest()
        
        audit_entry = {
            "Data": transaction,
            "Previous_Hash": self.last_log_hash,
            "Current_Hash": current_hash
        }
        self.audit_log.append(audit_entry)
        self.last_log_hash = current_hash 

# --- واجهة المستخدم الرسومية ---
class RiskGuardGUI:
    def __init__(self, root):
        self.system = RiskGuardSystem()
        self.root = root
        self.root.title("🛡️ RiskGuard Security System")
        self.root.geometry("850x650")
        self.root.configure(bg="#f4f6f9")
        
        # تحسين نمط الجداول والأزرار
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        self._create_widgets()
        
    def _create_widgets(self):
        # العنوان الرئيسي
        title_label = tk.Label(self.root, text="🛡️ RiskGuard: Maker-Checker & Audit System", font=("Arial", 16, "bold"), bg="#1e3d59", fg="white", pady=10)
        title_label.pack(fill=tk.X)
        
        # --- قسم إنشاء العمليات (Maker) ---
        maker_frame = tk.LabelFrame(self.root, text=" 📝 قسم إنشاء العمليات (Maker Panel) ", font=("Arial", 11, "bold"), bg="white", padx=10, pady=10)
        maker_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(maker_frame, text="اسم الموظف:", bg="white").grid(row=0, column=0, sticky="w")
        self.entry_maker = tk.Entry(maker_frame, width=20)
        self.entry_maker.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(maker_frame, text="المبلغ ($):", bg="white").grid(row=0, column=2, sticky="w")
        self.entry_amount = tk.Entry(maker_frame, width=15)
        self.entry_amount.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(maker_frame, text="الوصف:", bg="white").grid(row=0, column=4, sticky="w")
        self.entry_desc = tk.Entry(maker_frame, width=25)
        self.entry_desc.grid(row=0, column=5, padx=5, pady=5)
        
        btn_create = tk.Button(maker_frame, text="إنشاء عملية", command=self.create_tx, bg="#17b978", fg="white", font=("Arial", 10, "bold"))
        btn_create.grid(row=0, column=6, padx=10)

        # --- قسم العمليات المعلقة والاعتماد (Checker) ---
        checker_frame = tk.LabelFrame(self.root, text=" 🔍 قسم مراجعة العمليات والاعتماد (Checker Panel) ", font=("Arial", 11, "bold"), bg="white", padx=10, pady=10)
        checker_frame.pack(fill=tk.X, padx=15, pady=5)
        
        tk.Label(checker_frame, text="اسم المشرف/المدقق:", bg="white").grid(row=0, column=0, sticky="w")
        self.entry_checker = tk.Entry(checker_frame, width=20)
        self.entry_checker.grid(row=0, column=1, padx=5, pady=5)
        
        btn_approve = tk.Button(checker_frame, text="اعتماد (Approve)", command=lambda: self.verify_tx("approve"), bg="#438a5e", fg="white", font=("Arial", 10, "bold"))
        btn_approve.grid(row=0, column=2, padx=5)
        
        btn_reject = tk.Button(checker_frame, text="رفض (Reject)", command=lambda: self.verify_tx("reject"), bg="#ff4b5c", fg="white", font=("Arial", 10, "bold"))
        btn_reject.grid(row=0, column=3, padx=5)

        # جدول العمليات المعلقة
        tk.Label(self.root, text="⏳ العمليات المعلقة في انتظار المراجعة:", font=("Arial", 10, "bold"), bg="#f4f6f9").pack(anchor="w", padx=15)
        self.pending_tree = ttk.Treeview(self.root, columns=("ID", "Maker", "Amount", "Risk", "Desc"), show="headings", height=5)
        self.pending_tree.pack(fill=tk.X, padx=15, pady=5)
        for col, head in [("ID", "رقم العملية"), ("Maker", "الصانع"), ("Amount", "المبلغ"), ("Risk", "المخاطر"), ("Desc", "الوصف")]:
            self.pending_tree.heading(col, text=head)
            self.pending_tree.column(col, width=120, anchor="center")

        # --- قسم سجل التدقيق المشفر (Audit Trail) ---
        tk.Label(self.root, text="📊 سجل التدقيق الأمني المشفر (Immutable Audit Trail - Blockchain Logs):", font=("Arial", 10, "bold"), bg="#f4f6f9").pack(anchor="w", padx=15)
        self.audit_text = tk.Text(self.root, height=12, bg="#222831", fg="#00adb5", font=("Consolas", 10))
        self.audit_text.pack(fill=tk.BOTH, padx=15, pady=5, expand=True)

    def create_tx(self):
        try:
            maker = self.entry_maker.get()
            amount = float(self.entry_amount.get())
            desc = self.entry_desc.get()
            if not maker or not desc:
                raise ValueError("يرجى ملء جميع الحقول")
            
            tx_id = self.system.create_transaction(maker, amount, desc)
            tx = self.system.pending_requests[tx_id]
            self.pending_tree.insert("", "end", iid=tx_id, values=(tx_id, tx["Maker"], f"${tx['Amount']}", tx["Risk_Level"], tx["Description"]))
            
            # تفريغ الحقول
            self.entry_amount.delete(0, tk.END)
            self.entry_desc.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("خطأ", str(e))

    def verify_tx(self, action):
        selected_item = self.pending_tree.selection()
        if not selected_item:
            messagebox.showwarning("تنبيه", "يرجى اختيار عملية من الجدول أولاً!")
            return
        
        tx_id = selected_item[0]
        checker = self.entry_checker.get()
        if not checker:
            messagebox.showwarning("تنبيه", "يرجى إدخال اسم المشرف/المدقق!")
            return
            
        success, msg = self.system.verify_transaction(tx_id, checker, action)
        if success:
            messagebox.showinfo("نجاح", msg)
            self.pending_tree.delete(tx_id)
            self.update_audit_trail_view()
        else:
            messagebox.showerror("انتهاك أمني / خطأ", msg)

    def update_audit_trail_view(self):
        self.audit_text.delete("1.0", tk.END)
        for entry in self.system.audit_log:
            data = entry['Data']
            log_block = (
                f"📝 [ID: {data['Transaction_ID']}] | الحالة: {data['Status']}\n"
                f"   الصانع: {data['Maker']} | المدقق: {data['Checker']} | المبلغ: ${data['Amount']}\n"
                f"   🔗 الـ Hash الحالي: {entry['Current_Hash']}\n"
                f"   ⛓️ الـ Hash السابق: {entry['Previous_Hash']}\n"
                f"{'-'*95}\n"
            )
            self.audit_text.insert(tk.END, log_block)

if __name__ == "__main__":
    root = tk.Tk()
    app = RiskGuardGUI(root)
    root.mainloop()


# In[ ]:




