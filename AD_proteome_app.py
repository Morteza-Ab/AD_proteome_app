import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dataset1 = pd.read_excel('/Users/mortezaabyadeh/Downloads/Dataset1.xlsx')
dataset2 = pd.read_excel('/Users/mortezaabyadeh/Downloads/Dataset2.xlsx')
dataset3 = pd.read_excel('/Users/mortezaabyadeh/Downloads/Dataset3.xlsx')
dataset4 = pd.read_excel('/Users/mortezaabyadeh/Downloads/Dataset4.xlsx')
dataset5 = pd.read_excel('/Users/mortezaabyadeh/Downloads/Dataset5.xlsx')
dataset6 = pd.read_excel('/Users/mortezaabyadeh/Downloads/Dataset6.xlsx')
dataset7 = pd.read_excel('/Users/mortezaabyadeh/Downloads/Dataset7.xlsx')

datasets = {
    'Dataset 1': dataset1,
    'Dataset 2': dataset2,
    'Dataset 3': dataset3,
    'Dataset 4': dataset4,
    'Dataset 5': dataset5,
    'Dataset 6': dataset6,
    'Dataset 7': dataset7,
}

def display_footer():
    st.markdown("""
    <footer style='text-align: center; padding: 10px;'>
        <p>Please cite the following paper: 
        <a href="https://www.biorxiv.org/content/10.1101/2024.05.10.593647v1" target="_blank">
        Application of Multiomics Approach to Investigate the Therapeutic Potentials of Stem Cell-derived Extracellular Vesicle Subpopulations for Alzheimer’s Disease; Morteza Abyadeh, Alaattin Kaya; 2024</a>
        </p>
    </footer>
    """, unsafe_allow_html=True)

def main():
    st.title("Proteomics Data Viewer")
    
    st.sidebar.header("Input Options")
    protein_names = st.sidebar.text_area("Enter Up to 10 Protein Names (one per line or separated by commas)")

    st.sidebar.subheader("Visualization Options")
    show_scatter = st.sidebar.checkbox("Show Scatter Plot", value=True)  

    if protein_names:
        protein_names_list = [name.strip() for name in protein_names.split('\n') if name.strip()]
        
        for protein_name in protein_names_list:
            st.subheader(f"Search Results for: {protein_name}")
        
            results = {}
            protein_found = False  
            
            for name, data in datasets.items():
                result = data[data['Protein name'].str.fullmatch(protein_name, case=False, na=False)]
                if not result.empty:
                    protein_found = True
                    p_value = result['P-value'].values[0]
                    fold_change = result['Fold change'].values[0]
                    log10_pvalue = -np.log10(p_value)
                    results[name] = {'P-value': log10_pvalue, 'Fold change (log2)': fold_change}
            
            if protein_found:
                result_df = pd.DataFrame.from_dict(results, orient='index')
                result_df.reset_index(inplace=True)
                result_df.columns = ['Dataset', 'log10 P-value', 'log2 Fold change']
                result_df.insert(0, 'Gene name', protein_name)

                st.write("Search Results Table:")
                st.write(result_df)

                st.write(f"Download the results for {protein_name} as an Excel file:")
                if st.button(f'Generate Excel file for {protein_name}'):
                    result_df.to_excel(f"{protein_name}_results.xlsx", index=False)
                    with open(f"{protein_name}_results.xlsx", 'rb') as file:
                        btn = st.download_button(
                            label=f"Download Excel for {protein_name}",
                            data=file,
                            file_name=f"{protein_name}_results.xlsx",
                            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                        )

                if show_scatter:
                    st.subheader(f"Scatter Plot for {protein_name}")
                    plot_title = f"Scatter Plot for {protein_name}"
                    plt.figure(figsize=(8, 6))
                    for dataset, values in results.items():
                        if values['P-value'] != 'Not found' and values['Fold change (log2)'] != 'Not found':
                            plt.scatter(values['P-value'], values['Fold change (log2)'], marker='o', label=dataset, alpha=0.5)
                    plt.title(plot_title)
                    plt.xlabel('log10 P-value')
                    plt.ylabel('log2 Fold change')
                    plt.legend()
                    plt.grid(True)
                    st.pyplot(plt)
            else:
                st.write(f"Protein {protein_name} was not found in any of the datasets.")

    display_footer()

if __name__ == "__main__":
    main()
