#Install Packages for Analysis
install.packages("ggplot2")
install.packages("readxl")
install.packages("Rcpp")
install.packages("dplyr")

#Check Installed Packages
installed.packages()

#Call the above packages into the workspace
library(ggplot2)
library(dplyr)
library(readxl)
library(scales)

#Read CSV sheets into the workspace as dataframes

customer_df <- read.csv('C:\\Repos\\smart-store-justindavidson\\data\\prepared\\customers_prepared.csv')
product_df <- read.csv('C:\\Repos\\smart-store-justindavidson\\data\\prepared\\products_prepared.csv')
sale_df <- read.csv('C:\\Repos\\smart-store-justindavidson\\data\\prepared\\sales_prepared.csv')

# Join all data: sales + products + customers (to get region)
full_data <- sale_df %>%
  left_join(product_df, by = "product_id") %>%
  left_join(customer_df, by = "customer_id")

# Filter for Electronics category
electronics_sales <- full_data %>%
  filter(category == "Electronics")

# Remove duplicate product_id per region to avoid double-counting
electronics_unique <- electronics_sales %>%
  distinct(region, product_id, .keep_all = TRUE)

# Calculate total sales per row
electronics_unique <- electronics_unique %>%
  mutate(
    unit_price = as.numeric(gsub("[^0-9.]", "", unit_price)),
    amt_sold_fiscal_year = as.numeric(amt_sold_fiscal_year),
    total_sales_fy = unit_price * amt_sold_fiscal_year
  )

# Drop rows that return NA values post-data cleaning

electronics_unique <- electronics_unique %>%
  mutate(
    amt_sold_fiscal_year = gsub(",", "", amt_sold_fiscal_year),   
    amt_sold_fiscal_year = as.numeric(amt_sold_fiscal_year)       
  ) %>%
  filter(!is.na(amt_sold_fiscal_year)) %>%                        
  mutate(
    total_sales_fy = unit_price * amt_sold_fiscal_year           
  )

# Group by region and summarize

sales_by_region <- electronics_unique %>%
  filter(!is.na(region)) %>% 
  group_by(region) %>%
  summarise(total_sales_fy = sum(total_sales_fy, na.rm = TRUE)) %>%
  arrange(desc(total_sales_fy))

# ggplot bar chart visual

ggplot(sales_by_region, aes(x = reorder(region, -total_sales_fy), y = total_sales_fy, fill = region)) +
  geom_bar(stat = "identity") +
  geom_text(
    aes(label = label_dollar()(total_sales_fy)),
    color = "white",
    fontface = "bold",
    vjust = 2.5,  
    size = 4
  ) +
  scale_fill_brewer(palette = "Set2") + 
  labs(
    title = "Total Electronics Sales by Region (Fiscal Year)",
    x = "Region",
    y = "Total Sales ($)",
    fill = "Region"
  ) +
  scale_y_continuous(labels = label_dollar()) +
  theme_minimal() +
  theme(
    text = element_text(size = 12),
    axis.text.x = element_text(angle = 45, hjust = 1)
  )








