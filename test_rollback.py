import frappe

invs = [
    {'name': ('SINV-24-00009', 'SI/24-25/00005', 'SINV-24-00006')},
    {'name': ('SI/24-25/00004', 'SI/24-25/00003', 'SINV-24-00008')}
]


# Function to submit an invoice
def submit_invoice(inv_name):
    try:
        if inv_name not in ['SINV-24-00006']:
            inv = frappe.get_doc('Sales Invoice', inv_name)
            inv.submit()
            print(f"Submitted invoice: {inv_name}")
            return inv_name
        else:
            return None
    except Exception as e:
        print(f"Error submitting invoice {inv_name}: {str(e)}")
        return None


# # Function to rollback invoices
# def rollback_invoices(invs_to_rollback):
#     for inv_name in invs_to_rollback:
#         try:
#             frappe.db.rollback()
#             print(f"Rolled back invoice: {inv_name}")
#         except Exception as e:
#             print(f"Error rolling back invoice {inv_name}: {str(e)}")


@frappe.whitelist()
def try_rollback():
    # Iterate over each dictionary in invs
    for inv_dict in invs:
        frappe.db.savepoint("test_rollback")
        submitted_invs = []
        try:
            for inv_name in inv_dict['name']:
                try:
                    submitted_inv = submit_invoice(inv_name)
                    if submitted_inv:
                        submitted_invs.append(submitted_inv)
                    else:
                        # If submission fails, rollback previously submitted invoices and exit the loop
                        frappe.db.rollback(save_point="test_rollback")
                        break
                except Exception as e:
                    # If submission fails, rollback previously submitted invoices and exit the loop
                    frappe.db.rollback(save_point="test_rollback")
                    print(e)
                    break
            else:
                # If all invoices are successfully submitted, print a success message
                print("All invoices submitted successfully")
        except Exception as e:
            print(f"Error occurred while submitting invoices in dict {inv_dict}: {str(e)}")

    # Print the list of submitted invoices
    print("Submitted invoices:", submitted_invs)
