import sqlite3 # banco de dados
import tkinter as tk # lib de interface gráfica
from tkinter import messagebox, ttk # caixa de msg / tkinter


def conectar():
    return sqlite3.connect('xyz_comercio.db')


# banco de dados
def criar_tabela():
    conn = conectar()
    c = conn.cursor() # digitar sql num arquivo python
    c.execute('''
               CREATE TABLE IF NOT EXISTS clientes(

              cpf TEXT PRIMARY KEY,
              nome TEXT NOT NULL,
              email TEXT NOT NULL,
              telefone TEXT NOT NULL,
              endereco TEXT NOT NULL

              )''')
    conn.commit()
    conn.close()


# CREATE CRUD

def inserir_cliente():
    cpf      = entry_cpf.get().strip()
    nome     = entry_nome.get().strip()
    email    = entry_email.get().strip()
    telefone = entry_telefone.get().strip()
    endereco = entry_endereco.get().strip()

    if cpf and nome and email and telefone and endereco:
        try:
            conn = conectar()
            c = conn.cursor()
            c.execute('INSERT INTO clientes (cpf, nome, email, telefone, endereco) VALUES (?,?,?,?,?)',
                      (cpf, nome, email, telefone, endereco))
            conn.commit()
            conn.close()
            messagebox.showinfo('Dados', 'DADOS INSERIDOS COM SUCESSO!')
            mostra_clientes()
            limpar_campos()
        except sqlite3.IntegrityError:
            messagebox.showerror('Erro', 'ESTE CPF JÁ ESTÁ CADASTRADO NO SISTEMA!')
        except sqlite3.Error as e:
            messagebox.showerror('Erro', f'OCORREU UM ERRO AO INSERIR OS DADOS: {e}')
    else:
        messagebox.showwarning('Dado', 'INSIRA TODOS OS DADOS')


def mostra_clientes():
    for row in tree.get_children():
        tree.delete(row)
    conn = conectar()
    c = conn.cursor()
    c.execute('SELECT * FROM clientes')
    clientes = c.fetchall()
    for cliente in clientes:
        tree.insert('', 'end', values=cliente)
    conn.close()


def preencher_campos_ao_clicar(event):
    selecao = tree.selection()
    if selecao:
        limpar_campos()
        valores = tree.item(selecao)['values']

        entry_cpf.insert(0, valores[0])
        entry_nome.insert(0, valores[1])
        entry_email.insert(0, valores[2])
        entry_telefone.insert(0, valores[3])
        entry_endereco.insert(0, valores[4])


# ATUALIZAR
def editar_cliente():
    selecao = tree.selection()
    if selecao:
        cliente_cpf = tree.item(selecao)['values'][0]

        novo_nome     = entry_nome.get().strip()
        novo_email    = entry_email.get().strip()
        novo_telefone = entry_telefone.get().strip()
        novo_endereco = entry_endereco.get().strip()

        if novo_nome and novo_email and novo_telefone and novo_endereco:
            try:
                conn = conectar()
                c = conn.cursor()
                c.execute('''UPDATE clientes
                             SET nome = ?, email = ?, telefone = ?, endereco = ?
                             WHERE cpf = ?''',
                          (novo_nome, novo_email, novo_telefone, novo_endereco, cliente_cpf))
                conn.commit()
                conn.close()
                messagebox.showinfo('Dados', 'DADOS ATUALIZADOS COM SUCESSO!')
                mostra_clientes()
                limpar_campos()
            except sqlite3.Error as e:
                messagebox.showerror('Erro', f'OCORREU UM ERRO AO ATUALIZAR OS DADOS, VERIFIQUE: {e}')
        else:
            messagebox.showwarning('Dado', 'INSIRA TODOS OS DADOS')
    else:
        messagebox.showwarning('Aviso', 'SELECIONE UM CLIENTE NA TABELA PARA EDITAR.')


# DELETAR
def deletar_cliente():
    selecao = tree.selection()
    if selecao:
        resposta = messagebox.askyesno('Confirmar Exclusão', 'TEM CERTEZA QUE DESEJA EXCLUIR ESTE CLIENTE?')
        if resposta:
            cliente_cpf = tree.item(selecao)['values'][0]
            try:
                conn = conectar()
                c = conn.cursor()
                c.execute('DELETE FROM clientes WHERE cpf = ?', (cliente_cpf,))
                conn.commit()
                conn.close()
                messagebox.showinfo('Dados', 'DADOS DELETADOS COM SUCESSO!')
                mostra_clientes()
                limpar_campos()
            except sqlite3.Error as e:
                messagebox.showerror('Erro', f'ERRO AO DELETAR: {e}')
    else:
        messagebox.showerror('Dados', 'ERRO AO DELETAR OS DADOS! SELECIONE UM CLIENTE.')


def limpar_campos():
    entry_cpf.delete(0, tk.END)
    entry_nome.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)
    entry_endereco.delete(0, tk.END)


# interface grafica
janela = tk.Tk()
janela.geometry('800x600')
janela.title('XYZ Comércio - Cadastro de Clientes')

style = ttk.Style()
style.theme_use('clam')
style.configure('TLabel',           background='white', font=('arial', 10))
style.configure('TEntry',           font=('Segoe UI', 10))
style.configure('TButton',          font=('Segoe UI', 10), padding=6)
style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'))
style.configure('Treeview',         font=('Segoe UI', 10, 'bold'))


# frames - sessão
main_frame = ttk.Frame(janela, padding=15)
main_frame.pack(fill=tk.BOTH, expand=True)


# widgets - elementos
titulo = ttk.Label(main_frame, text='XYZ Comércio - Sistema de Cadastro de Clientes', font=('Segoe UI', 10, 'bold'))
titulo.grid(row=0, columnspan=2, pady=(0, 15), sticky='w')

input_frame = ttk.LabelFrame(main_frame, text='DADOS DO CLIENTE', padding=10)
input_frame.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(0, 15))

# CPF
ttk.Label(input_frame, text='CPF').grid(row=0, column=0, padx=(0, 10), pady=5, sticky='e')

entry_cpf = ttk.Entry(input_frame, width=30)
entry_cpf.grid(row=0, column=1, padx=(0, 20), pady=5, sticky='w')

# NOME
ttk.Label(input_frame, text='NOME').grid(row=1, column=0, padx=(0, 10), pady=5, sticky='e')

entry_nome = ttk.Entry(input_frame, width=40)
entry_nome.grid(row=1, column=1, padx=(0, 20), pady=5, sticky='w')

# E-MAIL
ttk.Label(input_frame, text='E-MAIL').grid(row=2, column=0, padx=(0, 10), pady=5, sticky='e')

entry_email = ttk.Entry(input_frame, width=40)
entry_email.grid(row=2, column=1, padx=(0, 20), pady=5, sticky='w')

# TELEFONE
ttk.Label(input_frame, text='TELEFONE').grid(row=3, column=0, padx=(0, 10), pady=5, sticky='e')

entry_telefone = ttk.Entry(input_frame, width=30)
entry_telefone.grid(row=3, column=1, padx=(0, 20), pady=5, sticky='w')

# ENDEREÇO
ttk.Label(input_frame, text='ENDEREÇO').grid(row=4, column=0, padx=(0, 10), pady=5, sticky='e')

entry_endereco = ttk.Entry(input_frame, width=60)
entry_endereco.grid(row=4, column=1, padx=(0, 20), pady=5, sticky='w')


# botões
btn_frame = ttk.Frame(main_frame)
btn_frame.grid(row=2, column=0, columnspan=2, pady=(0, 15), sticky='ew')

btn_salvar = ttk.Button(btn_frame, text='CADASTRAR', command=inserir_cliente)
btn_salvar.pack(side=tk.LEFT, padx=5)

btn_atualizar = ttk.Button(btn_frame, text='ATUALIZAR', command=editar_cliente)
btn_atualizar.pack(side=tk.LEFT, padx=5)

btn_deletar = ttk.Button(btn_frame, text='DELETAR', command=deletar_cliente)
btn_deletar.pack(side=tk.LEFT, padx=5)

btn_limpar = ttk.Button(btn_frame, text='LIMPAR', command=limpar_campos)
btn_limpar.pack(side=tk.LEFT, padx=5)


# Treeview - visualizar os dados
tree_frame = ttk.Frame(main_frame)
tree_frame.grid(row=3, column=0, columnspan=2, sticky='nsew')

main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure(3, weight=1)

# criação da TreeView
columns = ('CPF', 'NOME', 'E-MAIL', 'TELEFONE', 'ENDEREÇO')
tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=12)
tree.pack(fill=tk.BOTH, expand=True)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150, anchor='center')

# evento de clique na linha
tree.bind('<ButtonRelease-1>', preencher_campos_ao_clicar)

# scrollbar - barra rolagem
scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

criar_tabela()
mostra_clientes()

janela.mainloop()